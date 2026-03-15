"""
@file    preview_pane.py
@author  Rob Pellegrin
@date    03-11-2026

@updated 03-14-2026

"""

import curses

from ui.base_window import BaseWindow


class PreviewPane(BaseWindow):
    def create(self) -> None:
        left_width = self.width // 2
        right_width = self.width - left_width

        self.win = curses.newwin(self.height - 3, right_width, 0, left_width)

    def draw(self) -> None:
        self.win.box()
        self.win.addstr(0, 2, " Preview ", curses.color_pair(3))
