"""
@file    preview_pane.py
@author  Rob Pellegrin
@date    03-11-2026

@updated 03-11-2026

"""

import curses

from ui.base_window import BaseWindow


class PreviewPane(BaseWindow):
    def create(self):
        left_width = self.width // 2
        right_width = self.width - left_width

        self.win = curses.newwin(self.height - 3, right_width, 0, left_width)

    def refresh(self):
        self.win.erase()
        self.win.box()
        self.win.addstr(0, 2, " Preview ", curses.color_pair(3))

        self.win.noutrefresh()
