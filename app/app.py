"""
@file:    app.py
@author:  Rob Pellegrin
@date:    03-11-2026

TODO
    - Finish metadata.
    = Enter opens selected file.
    - File previews.
    - If len(query) > 1 and len(results) < 1, make query text red.

@updated: 03-16-2026

"""

import curses
import logging
import sys
from pathlib import Path

from ui.window_manager import WindowManager
from utils.config import Config
from utils.input_handler import InputHandler

logging.getLogger(__name__)


class App:
    def __init__(self, stdscr: curses.window) -> None:
        root = sys.argv[1] if len(sys.argv) > 1 else "."

        self.files = self.scan_files(root)
        self.stdscr = stdscr
        self.query = ""

        self.input = InputHandler(self)

        self.config = Config()

        self.wm = WindowManager(self)
        self.wm.create()

        self.cursor = 0

    def run(self) -> None:
        self.running = True

        while self.running:
            start_cursor = self.cursor

            key = self.stdscr.getch()

            self.input.handle(key)
            self.wm.refresh()

            # If the cursor moved, notify windows.
            if start_cursor != self.cursor:
                self.wm.details.needs_refresh = True

            curses.doupdate()

        self.config.save()

    def scan_files(self, root: str) -> list[Path]:
        files: list[Path] = []

        # Convert root to a Path object
        root_path = Path(root)

        # Using Path.rglob to walk through the directory
        # Use rglob to traverse through all files and directories
        # Skip cache files to prevent lots of garbage files.
        for entry in root_path.rglob("*"):
            if "cache" in str(entry).lower():
                continue

            try:
                if entry.is_file():
                    files.append(entry)  # Append the Path object directly
            except PermissionError:
                pass

        if len(files) > 1:
            files.sort()

        return files  # Ensure to return the list of Path objects
