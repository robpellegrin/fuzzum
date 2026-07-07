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
from typing import TYPE_CHECKING

from fuzzum.ui.panes.base_window import BaseWindow
from fuzzum.utils.curse_catcher import curse_catch

if TYPE_CHECKING:
    from fuzzum.app import App


class DetailsPane(BaseWindow):

    def __init__(self, app: "App") -> None:
        super().__init__(app)
        self.set_size()

    def set_size(self) -> None:
        screen_h, screen_w = self.app.stdscr.getmaxyx()

        self.height = 3
        self.width = screen_w - (screen_w // 2)

        self.x = self.width
        self.y = screen_h - 3

    @curse_catch
    def draw(self) -> None:
        super().draw()
        self.win.addstr(0, 2, "Details", curses.color_pair(3))

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
