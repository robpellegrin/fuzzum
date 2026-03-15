"""
@file    base_window.py
@author  Rob Pellegrin
@date    03-11-2026

@updated 03-14-2026

"""

import logging

logger = logging.getLogger(__name__)


class BaseWindow:

    def __init__(self, app, name: str):
        self.app = app

        self.win = None
        self.name = name
        self.needs_refresh = True

        try:
            self.visible = self.app.config.get("panes", self.name)
        except KeyError:
            self.visible = True

        self.height, self.width = self.stdscr.getmaxyx()

    @property
    def stdscr(self):
        return self.app.stdscr

    def toggle(self) -> None:
        self.visible = not self.visible
        self.app.config.set(self.visible, "panes", self.name)

    def resize(self, height, width) -> None:
        self.win.resize(height, width)

    def draw(self):
        raise NotImplementedError

    def refresh(self) -> None:
        if self.needs_refresh is False:
            return

        if self.visible is False:
            return

        self.draw()
        self.win.noutrefresh()
        self.needs_refresh = False

        logging.info("Refreshed %s", self.name)
