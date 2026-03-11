"""
@file    base_window.py
@author  Rob Pellegrin
@date    03-11-2026

@updated 03-11-2026

"""


class BaseWindow:
    def __init__(self, app, name: str):
        self.app = app
        self.stdscr = app.stdscr
        self.win = None
        self.name = name

        try:
            self.visible = self.app.config.get("panes", self.name)
        except KeyError:
            self.visible = True

        self.height, self.width = self.stdscr.getmaxyx()

    def toggle(self) -> None:
        self.visible = not self.visible
        self.app.config.set(self.visible, "panes", self.name)

    def resize(self, height, width) -> None:
        self.win.resize(height, width)

    def refresh(self) -> None:
        raise NotImplementedError
