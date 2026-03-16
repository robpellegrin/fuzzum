"""
@file    details_pane.py
@author  Rob Pellegrin
@date    03-11-2026

TODO:
    - Make output more attractive.
        + Human readable file sizes
        + Colors?

@updated 03-15-2026

"""

import curses
import logging
import os
import time

from ui.base_window import BaseWindow

logger = logging.getLogger(__name__)


class DetailsPane(BaseWindow):

    def create(self) -> None:
        self.win = curses.newwin(
            3, self.width // 2, self.height - 3, self.width // 2
        )

    def draw(self) -> None:
        self.win.erase()
        self.win.box()
        self.win.addstr(0, 2, " Details ", curses.color_pair(3))

        details_str: str = self._stat_file()

        self.win.addstr(1, 2, details_str)

    def _stat_file(self) -> str:
        """
        Gathers file metadata (size, last modified, etc) for a given
        file.

        """

        selected_file = self.app.wm.results.get_selected_file()

        try:
            info: os.stat_result = os.stat(selected_file)
        except FileNotFoundError:
            return "File not found!"
        except PermissionError:
            return "Permission Error!"

        # File size in bytes
        size: int = info.st_size

        # Last modification time (timestamp)
        mtime: str = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(info.st_mtime)
        )

        # Permissions as octal
        perms: str = oct(info.st_mode & 0o777)

        logger.debug("DetailsPane has file: %s", selected_file)

        self.needs_refresh = True

        return f"{size} {mtime} {perms}"
