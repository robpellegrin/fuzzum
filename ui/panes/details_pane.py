"""
@file    details_pane.py
@author  Rob Pellegrin
@date    03-11-2026

@updated 03-11-2026

"""

import curses
import os
import time

from ui.base_window import BaseWindow


class DetailsPane(BaseWindow):
    def create(self):
        self.win = curses.newwin(
            3, self.width // 2, self.height - 3, self.width // 2
        )

    def refresh(self):
        self.win.erase()
        self.win.box()
        self.win.addstr(0, 2, " Details ", curses.color_pair(3))

        self._stat_file()
        self.win.noutrefresh()

    def _stat_file(self):
        info = os.stat(self.app.files[self.app.cursor])

        # File size in bytes
        size = info.st_size

        # Last modification time (timestamp)
        mtime = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(info.st_mtime)
        )

        # Permissions as octal
        perms = oct(info.st_mode & 0o777)

        self.win.addstr(1, 2, f"{size} {mtime} {perms}")
