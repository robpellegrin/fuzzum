"""
@file    search_pane.py
@author  Rob Pellegrin
@date    03-11-2026

@updated 03-11-2026

"""

import curses

from ui.base_window import BaseWindow


class SearchPane(BaseWindow):
    def create(self):
        self.win = curses.newwin(3, self.width // 2, self.height - 3, 0)

    def refresh(self) -> None:
        self.win.erase()
        self.win.box()
        self.win.addstr(0, 2, " Search ", curses.color_pair(3))

    def update_query(self, query: str) -> None:
        self.win.addstr(1, 2, "> " + query, curses.color_pair(1))
        self.stdscr.move(self.height - 2, 4 + len(query))
        self.win.noutrefresh()

    def resize(self, height, width):
        self.win.resize(height, width)
