"""
@file    details_pane.py
@author  Rob Pellegrin
@date    03/11/2026

TODO:
    - Make output more attractive.
        + Human readable file sizes
        + Colors?

@updated 06/25/2026

"""

import curses
import datetime
import logging
import stat
from pathlib import Path

from fuzzum.ui.base_window import BaseWindow

logger = logging.getLogger(__name__)


class DetailsPane(BaseWindow):

    def create(self) -> None:
        self.win = curses.newwin(
            3, self.width // 2, self.height - 3, self.width // 2
        )

    def draw(self) -> None:
        super().draw()
        self.win.addstr(0, 2, " Details ", curses.color_pair(3))

        details_str: str = self._stat_file()

        self.win.addstr(1, 2, details_str)

    def _stat_file(self) -> str:
        """
        Gathers file metadata (size, last modified, etc) for a given
        file.

        """

        selected_file = self.app.files[self.app.cursor]

        try:
            st = Path(selected_file).stat()
        except FileNotFoundError:
            return "File not found!"
        except PermissionError:
            return "Permission Error!"

        perms = stat.filemode(st.st_mode)
        size = self._human_readable_size(st.st_size)
        mtime = datetime.datetime.fromtimestamp(st.st_mtime)
        mtime = mtime.strftime("%y-%m-%d %H:%M:%S")

        logger.debug("DetailsPane has file: %s", selected_file)

        self.needs_refresh = True

        return f"{perms} | {mtime} | {size}"

    @staticmethod
    def _human_readable_size(size: float) -> str:
        """
        Convert bytes into a human-readable format.

        :param size: Size in bytes
        :return: Human-readable representation of size

        """

        if size < 0:
            raise ValueError("Size must be a non-negative integer")

        units = ["B", "KB", "MB", "GB", "TB", "PB"]
        index = 0

        while size >= 1024 and index < len(units) - 1:
            size /= 1024
            index += 1

        # Remove trailing zeros.
        formatted = f"{size:.2f}".rstrip("0").rstrip(".")

        return f"{formatted}{units[index]}"
