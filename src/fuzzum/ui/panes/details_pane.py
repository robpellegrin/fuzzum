"""
@file    details_pane.py
@author  Rob Pellegrin
@date    03/11/2026

@updated 07/06/2026

"""

import curses
import datetime
import stat
from pathlib import Path

from fuzzum.ui.panes.base_window import BaseWindow
from fuzzum.utils.curse_catcher import curse_catch


class DetailsPane(BaseWindow):

    def create(self) -> None:
        self.win = curses.newwin(
            3, self.width // 2, self.height - 3, self.width // 2
        )

    @curse_catch
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

        if not (selected_file := self.app.files[self.app.cursor]):
            return "-"

        try:
            st = Path(selected_file).stat()
        except FileNotFoundError:
            return "File not found!"
        except PermissionError:
            return "Permission Error!"

        perms = stat.filemode(st.st_mode)
        size = self._human_readable_size(st.st_size)
        mtime = datetime.datetime.fromtimestamp(st.st_mtime)

        self.needs_refresh = True

        return f"{perms} | {mtime.strftime('%y-%m-%d %H:%M:%S')} | {size}"

    def _human_readable_size(self, size: float) -> str:
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
