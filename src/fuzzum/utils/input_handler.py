"""
@file    input_handler.py
@author  Rob Pellegrin
@date    03/11/2026

@updated 06/25/2026

"""

import curses
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fuzzum.app import App

CTRL_KEYS = {
    "CTRL_A": 1,
    "CTRL_B": 2,
    "CTRL_C": 3,
    "CTRL_D": 4,
    "CTRL_E": 5,
    "CTRL_H": 8,
    "CTRL_P": 16,
    "CTRL_T": 20,
    "CTRL_U": 21,
    "CTRL_Y": 25,
}


class InputHandler:
    def __init__(self, app: "App"):
        self.app = app

    def handle(self, key: int) -> None:
        ##
        # Special keys
        ##
        if key == ord("?"):
            self.app.wm.help.show()
            self.app.wm.previews.needs_refresh = True
            self.app.wm.results.needs_refresh = True

        # elif key == ord("."):
        #     self.app.wm.results.toggle_hidden_files()

        # elif key == ord(">"):
        #     self.app.wm.results.toggle_filenames()

        elif key == curses.KEY_BACKSPACE:
            self.app.query = self.app.query[:-1]
            self.app.needs_filter = True
            self.app.wm.search.needs_refresh = True

        ##
        # Navigation
        ##
        elif key in (curses.KEY_UP, CTRL_KEYS["CTRL_Y"]):
            self.app.wm.results.move_up()

        elif key in (curses.KEY_DOWN, CTRL_KEYS["CTRL_E"]):
            self.app.wm.results.move_down()

        elif key == curses.KEY_NPAGE:
            self.app.wm.results.page_down()

        elif key == curses.KEY_PPAGE:
            self.app.wm.results.page_up()

        elif key == curses.KEY_RESIZE:
            self.app.wm.resize()

        elif key == CTRL_KEYS["CTRL_P"]:
            self.app.wm.toggle_window(self.app.wm.previews)

        elif key == CTRL_KEYS["CTRL_D"]:
            self.app.wm.toggle_window(self.app.wm.details)

        elif key == CTRL_KEYS["CTRL_T"]:
            self.app.tclip()

        elif key == CTRL_KEYS["CTRL_U"]:
            self.app.query = ""
            self.app.wm.search.needs_refresh = True
            self.app.needs_filter = True

        elif 32 <= key <= 126:
            self.app.needs_filter = True
            self.app.wm.search.update_query(chr(key))
