"""
@file    base_window.py
@author  Rob Pellegrin
@date    03-11-2026

@updated 03-14-2026

"""

import curses
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.app import App


logger = logging.getLogger(__name__)


class BaseWindow:

    name: str
    needs_refresh: bool
    visible: bool

    win: curses.window

    def __init__(self, app: "App", name: str):
        self.app = app

        self.height, self.width = self.app.stdscr.getmaxyx()
        self.base_height = self.height

        self.needs_refresh = True
        self.name = name

        try:
            self.visible = self.app.config.get("panes", self.name)
        except KeyError:
            self.visible = True

    def toggle_visibility(self) -> None:
        self.visible = not self.visible
        self.app.config.set(self.visible, "panes", self.name)

    def resize(self, height: int, width: int) -> None:
        self.height = height
        self.width = width

        # Keep values used by parent class up to date.
        self.win.resize(height, width)

    def draw(self) -> None:
        raise NotImplementedError

    def create(self) -> None:
        raise NotImplementedError

    def refresh_window(self) -> None:
        if not self.needs_refresh or not self.visible:
            return

        self.draw()
        self.win.noutrefresh()
        self.needs_refresh = False

        logging.info("Refreshed %s", self.name)
