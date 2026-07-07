"""
@file    search_pane.py
@author  Rob Pellegrin
@date    03/11/2026

@updated 07/06/2026

"""

import curses
from typing import TYPE_CHECKING

from fuzzum.ui.panes.base_window import BaseWindow
from fuzzum.utils.curse_catcher import curse_catch

if TYPE_CHECKING:
    from fuzzum.app import App


class SearchPane(BaseWindow):

    def __init__(self, app: "App") -> None:
        super().__init__(app)
        self.query_text_color: int

        self.set_size()

    def create(self) -> None:
        self.win = curses.newwin(self.height, self.width, self.y, self.x)

    def set_size(self) -> None:
        screen_h, screen_w = self.app.stdscr.getmaxyx()

        self.height = 3
        self.width = screen_w // 2

        self.x = 0
        self.y = screen_h - self.height

    @curse_catch
    def draw(self) -> None:
        super().draw()

        self.win.addstr(0, 2, "Search", curses.color_pair(3))
        self.win.addstr(1, 2, "> " + self.app.query, self.query_text_color)

    def update_query(self, query: str) -> None:
        self.app.query += query
        self.needs_refresh = True

    def get_cursor_position(self) -> tuple[int, int]:
        return (
            self.y + 1,
            self.x + len(self.app.query) + 4,
        )
