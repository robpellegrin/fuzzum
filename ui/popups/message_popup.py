"""
@file    message_popup.py
@author  Rob Pellegrin
@date    03-16-2026

@updated 03-16-2026

"""


class MessagePopup:

    def __init__(self, parent):
        self.parent = parent

    def show_message(self, message: str) -> None:
        h, w = self.parent.win.getmaxyx()

        popup_h = 5
        popup_w = min(len(message) + 6, w - 4)

        y = (h - popup_h) // 2
        x = (w - popup_w) // 2

        popup = self.parent.win.derwin(popup_h, popup_w, y, x)

        popup.erase()
        popup.box()

        popup.addstr(2, 2, message[: popup_w - 4])

        popup.refresh()
