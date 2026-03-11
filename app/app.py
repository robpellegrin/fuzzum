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

from ui.help_popup import HelpPopup
from ui.window_manager import WindowManager
from utils.config import Config
from utils.input_handler import InputHandler


class App:
    def __init__(self, stdscr):
        root = sys.argv[1] if len(sys.argv) > 1 else "."

        self.files = self.scan_files(root)
        self.stdscr = stdscr

        self.input = InputHandler(self)

        curses.curs_set(1)
        curses.start_color()
        curses.use_default_colors()

        stdscr.nodelay(True)
        stdscr.timeout(25)

        curses.init_pair(1, curses.COLOR_CYAN, -1)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_YELLOW, -1)

        self.wm = WindowManager(self)
        self.wm.create()

        self.cursor = 0

    @property
    def config(self):
        return Config()

    @property
    def help(self):
        return HelpPopup(self)

    def run(self):
        self.query = ""
        self.running = True

        while self.running:
            key = self.stdscr.getch()

            self.wm.search.update_query(self.query)

            self.input.handle(key)
            self.wm.refresh()

    def scan_files(self, root):
        files = []

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
