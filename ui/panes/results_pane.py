"""
@file    results_pane.py
@author  Rob Pellegrin
@date    03-11-2026

@updated 03-16-2026

"""

import curses
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Union

from ui.base_window import BaseWindow
from utils.file_filter import FileFilter

if TYPE_CHECKING:
    from app.app import App

logger = logging.getLogger(__name__)


class ResultsPane(BaseWindow):
    """Scrollable results pane with highlight and vertical scrollbar."""

    def __init__(self, app: "App", name: str) -> None:
        super().__init__(app, name)

        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        self.files = FileFilter(self.app.files, self.app.config)

        self.offset = 0  # top visible item
        self.cursor = 0  # selected item

    def get_selected_file(self) -> Union[list[Path], Path]:
        return self.files[self.cursor]

    def create(self) -> None:
        self.win = curses.newwin(self.height - 3, self.width // 2, 0, 0)

    def header(self, results_count: int = 0) -> None:
        self.win.addstr(
            0, 1, f" Results —— ({results_count:,d}) ", curses.color_pair(3)
        )

    def draw(self) -> None:
        self.win.erase()
        self.win.box()
        self.header(len(self.files))

        self._draw_files()
        self._draw_scrollbar()

        self.cursor = min(self.cursor, len(self.files) - 1)
        self.cursor = max(self.cursor, 0)
        self.app.cursor = self.cursor

    def toggle_filenames(self) -> None:
        self.files.show_filename_only = not self.files.show_filename_only
        self.needs_refresh = True

    def toggle_hidden_files(self) -> None:
        self.files.show_hidden_files = not self.files.show_hidden_files
        self.needs_refresh = True

    def _draw_files(self) -> None:
        max_rows: int = self.height - 2
        max_width: int = self.width - 5

        visible: list[Path] = self.files[
            self.offset: self.offset + max_rows
        ]

        for i, filename in enumerate(visible):
            if self.files.show_filename_only:
                file = filename.name
            else:
                file = str(filename)

            row: int = i + 1
            text: str = file[:max_width]

            try:
                if self.offset + i == self.cursor:
                    self.win.addstr(row, 1, "〉" + text, curses.color_pair(4))
                else:
                    self.win.addstr(row, 3, text)
            except curses.error as e:
                logging.error("_draw_files: %s", e)

    def _draw_scrollbar(self) -> None:
        visible_rows = self.height - 2
        total_items = len(self.files)

        if total_items <= visible_rows:
            return

        scrollbar_x = self.width - 2
        scrollbar_height = visible_rows

        # Thumb size proportional to visible content.
        thumb_size = max(
            1,
            int(scrollbar_height * (visible_rows / total_items))
        )

        max_offset = total_items - visible_rows

        thumb_pos = int(
            (self.offset / max_offset)
            * (scrollbar_height - thumb_size)
        )

        for i in range(scrollbar_height):
            char = "│"

            if thumb_pos <= i < thumb_pos + thumb_size:
                char = "█"

            try:
                self.win.addstr(i + 1, scrollbar_x, char)
            except curses.error as e:
                logger.error("draw_scrollbar: %s", e)

    ##
    # Scrolling
    ##
    def move_down(self) -> None:
        if 0 <= self.cursor < len(self.files) - 1:
            self.cursor += 1
            self._adjust_offset()

    def move_up(self) -> None:
        if 0 < self.cursor <= len(self.files):
            self.cursor -= 1
            self._adjust_offset()

    def page_down(self) -> None:
        if self.cursor == len(self.files) - 1:
            return

        page = self.win.getmaxyx()[0] - 2
        self.cursor = min(len(self.files) - 1, self.cursor + page)
        self._adjust_offset()

    def page_up(self) -> None:
        if self.cursor == 0:
            return

        page = self.win.getmaxyx()[0] - 2
        self.cursor = max(0, self.cursor - page)
        self._adjust_offset()

    def go_top(self) -> None:
        self.cursor = 0
        self._adjust_offset()

    def go_bottom(self) -> None:
        self.cursor = len(self.files) - 1
        self._adjust_offset()

    def _adjust_offset(self) -> None:
        """Adjust the top-of-window offset to keep the cursor visible."""

        height = self.win.getmaxyx()[0] - 2

        if self.cursor < self.offset:
            self.offset = self.cursor

        elif self.cursor >= self.offset + height:
            self.offset = self.cursor - height + 1

        self.needs_refresh = True
