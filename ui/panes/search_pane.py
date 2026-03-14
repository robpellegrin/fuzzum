"""
@file    search_pane.py
@author  Rob Pellegrin
@date    03-11-2026

@updated 03-11-2026

"""

import curses
import sys

from ui.base_window import BaseWindow


class SearchPane(BaseWindow):

    def __init__(self, app, name):
        super().__init__(app, name)

    def create(self):
        self.win = curses.newwin(3, self.width // 2, self.height - 3, 0)
        self.win.box()

    def draw(self) -> None:
        self.win.addstr(0, 2, " Search ", curses.color_pair(3))
        self.win.addstr(1, 2, "> " + self.app.query, curses.color_pair(1))
        self.stdscr.move(self.height - 2, 4 + len(self.app.query))

    def update_query(self, query: str) -> None:
        self.app.query += query
        self.needs_refresh = True

    def resize(self, height, width):
        self.win.resize(height, width)
        self.needs_refresh = True

    def get_cursor_position(self):
        return (self.height - 2, 4 + len(self.app.query))
