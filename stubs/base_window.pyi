

import curses
from contextlib import contextmanager
from fuzzum.app.app import App as App
from typing import Any

@contextmanager
def curses_attr(win: curses.window, attr: int) -> Any: ...

class BaseWindow:
    win: curses.window
    app: App
    height: int
    width: int
    base_height: int
    needs_refresh: bool
    visible: bool
    name: str

    def __init__(self, app: App, name: str) -> None: ...
    def toggle_visibility(self) -> None: ...
    def resize(self, height: int, width: int) -> None: ...
    def draw(self) -> None: ...
    def create(self) -> None: ...
    def refresh_window(self) -> None: ...
