"""
@file    base_window.py
@author  Rob Pellegrin
@date    03/11/2026

@updated 06/25/2026

"""

import curses
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any

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
        self.win: curses.window
        self.app = app

        self.height: int
        self.width: int
        self.height, self.width = self.app.stdscr.getmaxyx()

        self.base_height: int = self.height

        self.needs_refresh = True
        self.visible: bool = True

    def toggle_visibility(self) -> None:
        self.visible = not self.visible
        self.app.config.set(self.visible, "panes", None)

    def resize(self, height: int, width: int) -> None:
        self.height = height
        self.width = width

        # Keep values used by parent class up to date.
        self.win.resize(height, width)

    def draw(self) -> None:
        self.win.erase()

        with curses_attr(self.win, curses.color_pair(0) | curses.A_DIM):
            self.win.box()

    def create(self) -> None:
        raise NotImplementedError

    def refresh_window(self) -> None:
        if not self.needs_refresh or not self.visible:
            return

        self.draw()
        self.win.noutrefresh()
        self.needs_refresh = False
