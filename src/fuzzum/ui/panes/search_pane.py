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
    def create(self) -> None:
        self.win = curses.newwin(3, self.width // 2, self.height - 3, 0)

    @curse_catch
    def draw(self) -> None:
        super().draw()

        self.win.addstr(0, 2, "Search", curses.color_pair(3))

        self.win.addstr(1, 2, "> " + self.app.query, self.query_text_color)

        self.app.stdscr.move(self.height - 2, len(self.app.query) + 4)

    def update_query(self, query: str) -> None:
        self.app.query += query
        self.needs_refresh = True

    def get_cursor_position(self) -> tuple[int, int]:
        return (self.height - 2, 4 + len(self.app.query))
