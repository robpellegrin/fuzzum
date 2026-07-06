"""
@file    results_pane.py
@author  Rob Pellegrin
@date    03/11/2026

@updated 06/27/2026

"""

import curses
from pathlib import Path
from typing import TYPE_CHECKING

from fuzzum.ui.panes.base_window import BaseWindow
from fuzzum.ui.scroll_bar import ScrollBar
from fuzzum.utils.curse_catcher import curse_catch

if TYPE_CHECKING:
    from fuzzum.app import App


class ResultsPane(BaseWindow):
    """Scrollable results pane with highlight and vertical scrollbar."""

    def __init__(self, app: "App") -> None:
        super().__init__(app)

        self.files = self.app.files

        self.offset = 0  # top visible item
        self.cursor = 0  # selected item

        self.set_size()

    def set_size(self) -> None:
        height, width = self.win.getmaxyx()

        self.height = height - 3
        self.width = width // 2

    @curse_catch
    def create(self) -> None:
        self.win = curses.newwin(self.height, self.width, 0, 0)

    @curse_catch
    def header(self, results_count: int = 0) -> None:
        self.win.addstr(
            0, 2, f"Results —— ({results_count:,d})", curses.color_pair(3)
        )

    def draw(self) -> None:
        super().draw()

        scroll_bar = ScrollBar(
            win=self.win,
            total_rows=len(self.files),
            offset=self.offset,
        )

        self.header(len(self.files))

        self._draw_files()
        scroll_bar.draw()

        self.cursor = min(self.cursor, len(self.files) - 1)
        self.cursor = max(self.cursor, 0)
        self.app.cursor = self.cursor

    @curse_catch
    def _draw_files(self) -> None:
        max_rows: int = self.height + 1
        max_width: int = self.width

        visible: list[Path] = self.files[self.offset: self.offset + max_rows]

        for i, filename in enumerate(visible):
            file = str(filename)

            row: int = i + 1
            text: str = file[:max_width]

            if self.offset + i == self.cursor:
                self.win.addstr(row, 1, "┃ " + text, curses.color_pair(4))
            else:
                self.win.addstr(row, 3, text)

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

        page = self.win.getmaxyx()[0] - 3
        self.cursor = min(len(self.files) - 1, self.cursor + page)
        self._adjust_offset()

    def page_up(self) -> None:
        if self.cursor == 0:
            return

        page = self.win.getmaxyx()[0] - 3
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
