"""
@file    search_pane.py
@author  Rob Pellegrin
@date    03/11/2026

@updated 06/25/2026

"""

import curses

from fuzzum.ui.panes.base_window import BaseWindow


class SearchPane(BaseWindow):

    def create(self) -> None:
        self.win = curses.newwin(3, self.width // 2, self.height - 3, 0)

    def draw(self) -> None:
        super().draw()

        self.win.addstr(0, 2, " Search ", curses.color_pair(3))

        # Write query text.
        self.win.addstr(1, 2, "> " + self.app.query, curses.color_pair(1))

        try:
            self.app.stdscr.move(self.base_height - 2, 4 + len(self.app.query))
        except Exception:
            pass

    def update_query(self, query: str) -> None:
        self.app.query += query
        self.needs_refresh = True

    def get_cursor_position(self) -> tuple[int, int]:
        return (self.base_height - 2, 4 + len(self.app.query))
