"""
@file    search_pane.py
@author  Rob Pellegrin
@date    03/11/2026

@updated 07/06/2026

"""

import curses

from fuzzum.ui.panes.base_window import BaseWindow
from fuzzum.utils.curse_catcher import curse_catch


class SearchPane(BaseWindow):

    def __init__(self, app) -> None:
        super().__init__(app)

        self.set_size()

    def create(self) -> None:
        self.win = self.app.stdscr.subwin(3, self.width, self.height, 0)

    def set_size(self) -> None:
        height, width = self.win.getmaxyx()

        self.height = height - 3
        self.width = width // 2

    def draw(self) -> None:
        super().draw()

        try:
            self.win.addstr(0, 2, "Search", curses.color_pair(3))
            self.win.addstr(1, 2, "> " + self.app.query, self.query_text_color)

            self.win.move(self.height + 1, len(self.app.query) + 4)
        except curses.error:
            pass

    def update_query(self, query: str) -> None:
        self.app.query += query
        self.needs_refresh = True

    def get_cursor_position(self) -> tuple[int, int]:
        return (self.height - 3, len(self.app.query) + 4)
