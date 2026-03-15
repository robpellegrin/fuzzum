"""
@file    input_handler.py
@author  Rob Pellegrin
@date    03-11-2026

@updated 03-14-2026

"""

import curses
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.app import App

CTRL_KEYS = {
    "CTRL_A": 1,
    "CTRL_B": 2,
    "CTRL_C": 3,
    "CTRL_D": 4,
    "CTRL_H": 8,
    "CTRL_P": 16,
    "CTRL_U": 21,
}


class InputHandler:
    def __init__(self, app: "App"):
        self.app = app

    def handle(self, key: int) -> None:
        ##
        # Special keys
        ##

        if key == ord("q") or key == 15:
            self.app.running = False

        elif key == ord("?"):
            self.app.wm.help.show()
            self.app.wm.refresh()

        elif key == ord("."):
            self.app.wm.results.toggle_hidden_files()

        elif key == ord(">"):
            self.app.wm.results.toggle_filenames()

        elif key == curses.KEY_BACKSPACE:
            self.app.query = self.app.query[:-1]
            self.app.wm.search.needs_refresh = True

        ##
        # Navigation
        ##
        elif key == curses.KEY_UP:
            self.app.wm.results.move_up()

        elif key == curses.KEY_DOWN:
            self.app.wm.results.move_down()

        elif key == curses.KEY_NPAGE:
            self.app.wm.results.page_down()

        elif key == curses.KEY_PPAGE:
            self.app.wm.results.page_up()

        elif key == curses.KEY_RESIZE:
            self.app.wm.resize()

        elif key == CTRL_KEYS["CTRL_P"]:
            self.app.wm.toggle_window(self.app.wm.previews)
            self.app.wm.resize()

        elif key == CTRL_KEYS["CTRL_D"]:
            self.app.wm.toggle_window(self.app.wm.details)
            self.app.wm.resize()

        elif key == CTRL_KEYS["CTRL_U"]:
            self.app.query = ""

        elif 32 <= key <= 126:
            self.app.wm.search.update_query(chr(key))
