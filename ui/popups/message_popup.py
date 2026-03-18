"""
@file    message_popup.py
@author  Rob Pellegrin
@date    03-16-2026

@updated 03-17-2026

"""
import curses
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.base_window import BaseWindow


class MessagePopup:

    def __init__(self, parent: "BaseWindow") -> None:
        self.parent = parent

    def show_message(self, message: str) -> None:
        h, w = self.parent.win.getmaxyx()

        curses.init_pair(1, curses.COLOR_BLUE, -1)

        popup_h = 5
        popup_w = min(len(message) + 6, w - 4)

        y = (h - popup_h) // 2
        x = (w - popup_w) // 2

        popup = self.parent.win.derwin(popup_h, popup_w, y, x)
        popup.erase()
        popup.addstr(2, 2, message[: popup_w - 4])

        popup.refresh()
