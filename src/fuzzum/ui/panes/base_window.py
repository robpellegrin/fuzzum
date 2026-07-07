"""
@file    base_window.py
@author  Rob Pellegrin
@date    03/11/2026

@updated 07/06/2026

"""

import curses
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any

from fuzzum.utils.curse_catcher import curse_catch

if TYPE_CHECKING:
    from fuzzum.app import App


@contextmanager
def curses_attr(win: curses.window, attr: int) -> Any:
    win.attron(attr)
    try:
        yield
    finally:
        win.attroff(attr)


class BaseWindow:

    def __init__(self, app: "App"):
        self.app = app
        self.win: curses.window

        self.height = 0
        self.width = 0

        self.x = 0
        self.y = 0

        self.needs_refresh = True
        self.visible: bool = True

    def set_size(self) -> None:
        raise NotImplementedError

    def create(self) -> None:
        self.win = curses.newwin(self.height, self.width, self.y, self.x)

    def toggle_visibility(self) -> None:
        self.visible = not self.visible
        self.app.config.set(self.visible, "panes", __file__)

    @curse_catch
    def draw(self) -> None:
        self.win.erase()

        with curses_attr(self.win, curses.color_pair(0) | curses.A_DIM):
            self.win.box()

    def refresh_window(self) -> None:
        if not self.needs_refresh or not self.visible:
            return

        self.draw()
        self.win.noutrefresh()
        self.needs_refresh = False
