"""
@file:    app.py
@author:  Rob Pellegrin
@date:    03/11/2026

TODO
    - If len(query) > 1 and len(results) < 1, make query text red.

@updated 06/30/2026

"""

import argparse
import curses
import logging
import os
import subprocess
from pathlib import Path

from fuzzum.ui.window_manager import WindowManager
from fuzzum.utils.config import Config
from fuzzum.utils.file_filter import FileFilter
from fuzzum.utils.input_handler import InputHandler

logging.getLogger(__name__)


class App:
    def __init__(
        self, stdscr: curses.window, args: argparse.Namespace
    ) -> None:
        root = args.path

        self.needs_filter = True
        self.cursor = 0
        self.query = ""

        self.stdscr = stdscr

        self.input = InputHandler(self)
        self.config = Config()
        self.files = FileFilter(self.scan_files(root, max_depth=args.depth))

        self.wm = WindowManager(self)

    def run(self) -> Path:
        self.running = True

        while (key := self.stdscr.getch()) != ord("q"):
            start_cursor = self.cursor

            self.input.handle(key)
            self.wm.refresh()

            # If the cursor moved, notify windows.
            if start_cursor != self.cursor:
                self.wm.details.needs_refresh = True
                self.wm.previews.needs_refresh = True

            if self.needs_filter:
                self.files.filter(self.query)
                self.needs_filter = False
                self.wm.results.needs_refresh = True

            curses.doupdate()

            if not self.running:
                break

        self.config.save()

        selected_file: Path = self.files[self.cursor]

        return selected_file

    def tclip(self) -> int:
        selection = self.files[self.cursor]
        returncode = -1

        try:
            cmd = subprocess.run(
                [
                    "tmux",
                    "set-buffer",
                    "--",
                    selection,
                ],
                stderr=subprocess.DEVNULL,
                check=True,
            )

            returncode = cmd.returncode

        except subprocess.CalledProcessError:
            pass

        return returncode

    def scan_files(self, start_dir: Path, max_depth: int) -> list[Path]:
        files: list[Path] = []
        stack: list[tuple[str, int]] = [(str(start_dir), 0)]

        while stack:
            current_dir: str
            depth: int

            current_dir, depth = stack.pop()

            try:
                with os.scandir(current_dir) as entries:
                    for entry in entries:
                        if entry.is_file(follow_symlinks=False):
                            files.append(Path(entry.path))
                            continue

                        if not entry.is_dir(follow_symlinks=False):
                            continue

                        if depth < max_depth:
                            stack.append((entry.path, depth + 1))
            except PermissionError:
                continue

        return files
