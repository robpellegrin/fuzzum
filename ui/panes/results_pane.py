"""
@file    results_pane.py
@author  Rob Pellegrin
@date    03-11-2026

@updated 03-14-2026

"""

import curses
import logging
from pathlib import Path
from typing import TYPE_CHECKING

from ui.base_window import BaseWindow

if TYPE_CHECKING:
    from app.app import App

logger = logging.getLogger(__name__)


class ResultsPane(BaseWindow):
    """Scrollable results pane with highlight and vertical scrollbar."""

    def __init__(self, app: "App", name: str) -> None:
        super().__init__(app, name)

        self.offset = 0  # top visible item
        self.cursor = 0  # selected item

        self.files: list[str] = self.app.files

        self.show_filenames_only: bool = (
            self.app.config.get("ui", "show_filenames_only") or False
        )

        self.show_hidden_files: bool = (
            self.app.config.get("ui", "show_hidden_files") or False
        )

        self._filter_files()

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
        self.app.cursor = self.cursor

    def _filter_files(self) -> None:
        self.files = [
            Path(f).name if self.show_filenames_only else f
            for f in self.app.files
            if self.show_hidden_files or not self._is_hidden_path(f)
        ]

    def _is_hidden_path(self, path: str) -> bool:
        return any(part.startswith(".") for part in path.split("/"))

    def toggle_filenames(self) -> None:
        self.show_filenames_only = not self.show_filenames_only
        self._filter_files()
        self.needs_refresh = True

    def toggle_hidden_files(self) -> None:
        self.show_hidden_files = not self.show_hidden_files
        self._filter_files()
        self.needs_refresh = True

    def _draw_files(self) -> None:
        max_rows = self.height - 5
        max_width = self.width - 18

        visible = self.files[self.offset: self.offset + max_rows]

        for i, file in enumerate(visible):
            row = i + 1
            text = file[:max_width]

            try:
                if self.offset + i == self.cursor:
                    self.win.addstr(row, 2, text, curses.A_REVERSE)
                else:
                    self.win.addstr(row, 2, text)
            except curses.error:
                pass

    def _draw_scrollbar(self) -> None:
        max_rows = self.height - 5
        total_items = len(self.files)

        if total_items <= max_rows:
            return

        scrollbar_x = self.width - 2
        scrollbar_height = max_rows

        # Thumb size
        thumb_size = max(1, int(scrollbar_height * (max_rows / total_items)))

        # Thumb position
        thumb_pos = (
            int(
                (self.cursor / total_items)
                * (scrollbar_height - thumb_size))
            + 1
        )

        for i in range(scrollbar_height):
            char = "│"

            if thumb_pos <= i < thumb_pos + thumb_size:
                char = "█"

            try:
                self.win.addstr(i + 1, scrollbar_x, char)
            except curses.error:
                pass

    ##
    # Scrolling
    ##
    def move_down(self) -> None:
        if 0 <= self.cursor < len(self.files) - 1:
            self.cursor += 1
            self._adjust_offset()
            self.needs_refresh = True

    def move_up(self) -> None:
        if 0 < self.cursor <= len(self.files):
            self.needs_refresh = True
            self.cursor -= 1
            self._adjust_offset()

    def page_down(self) -> None:
        page = self.win.getmaxyx()[0] - 2
        self.cursor = min(len(self.app.files) - 1, self.cursor + page)
        self._adjust_offset()

    def page_up(self) -> None:
        page = self.win.getmaxyx()[0] - 2
        self.cursor = max(0, self.cursor - page)
        self._adjust_offset()

    def go_top(self) -> None:
        self.cursor = 0
        self._adjust_offset()

    def go_bottom(self) -> None:
        self.cursor = len(self.app.files) - 1
        self._adjust_offset()

    def _adjust_offset(self) -> None:
        """Adjust the top-of-window offset to keep the cursor visible."""

        h = self.win.getmaxyx()[0] - 2

        if self.cursor < self.offset:
            self.offset = self.cursor
        elif self.cursor >= self.offset + h:
            self.offset = self.cursor - h + 1
