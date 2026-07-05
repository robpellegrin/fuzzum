"""
@file:    app.py
@author:  Rob Pellegrin
@date:    03/11/2026

@updated 07/04/2026

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
        root: Path = args.path

        self.needs_filter = True
        self.cursor = 0
        self.query = ""

        self.stdscr = stdscr

        self.input = InputHandler(self)
        self.config = Config()
        self.files = FileFilter(self.scan_files(root, max_depth=args.depth))

        self.wm = WindowManager(self)

    def run(self) -> Path:
        """Main event loop for App."""

        # Track cursor changes.
        start_cursor: int = self.cursor

        while (key := self.stdscr.getch()) != ord("\n"):

            self.input.handle(key)

            # If the cursor moved, notify windows.
            if start_cursor != self.cursor:
                self.wm.details.needs_refresh = True
                self.wm.previews.needs_refresh = True

            if self.needs_filter:
                self.files.filter(self.query)
                self.needs_filter = False
                self.wm.results.needs_refresh = True

            if self.files:
                self.wm.search.query_text_color = curses.color_pair(1)
            else:
                self.wm.search.query_text_color = curses.color_pair(10)

            start_cursor = self.cursor
            self.wm.refresh()

        self.config.save()

        selected_file: Path = self.files[self.cursor]

        return selected_file

    def tclip(self) -> int:
        """Copies the path to the currently selected file into tmux buffer."""

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
        """
        Scans a directory tree and return all discovered files.

        Traverses the directory hierarchy rooted at ``start_dir`` using an
        iterative depth-first search. Symbolic links are not followed to avoid
        cycles and unintended traversal outside the target tree. Directories
        that cannot be accessed due to insufficient permissions are skipped.

        Args:
            start_dir: The root directory from which to begin scanning.
            max_depth: The maximum directory depth to traverse, relative to
                `start_dir`. A value of `0` scans only `start_dir` itself,
                while larger values allow traversal into nested sub
                directories.

        Returns:
            A list of :class:`pathlib.Path` objects representing all regular
            files found within the permitted traversal depth.
        """

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
