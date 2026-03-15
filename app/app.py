"""

TODO
    - Finish metadata.
    = Enter opens selected file.
    - File previews.
    - If len(query) > 1 and len(results) < 1, make query text red.

"""

import curses
import os
import sys

from ui.window_manager import WindowManager
from utils.config import Config
from utils.input_handler import InputHandler


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

    def scan_files(self, root: str) -> list[str]:
        files: list[str] = []

        with os.scandir(root) as entries:
            for entry in entries:
                # Skip cache files to prevent appearance of
                # lots of garbage files.
                if "cache" in entry.path.lower():
                    continue

                try:
                    # Remove leading "./" before appending.
                    if entry.is_file():
                        files.append(entry.path.removeprefix("./"))
                    elif entry.is_dir():
                        files.extend(self.scan_files(entry.path))
                except PermissionError:
                    pass

        if len(files) > 1:
            files.sort()

        return files
