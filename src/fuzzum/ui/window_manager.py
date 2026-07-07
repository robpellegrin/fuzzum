"""
@file    window_manager.py
@author  Rob Pellegrin
@date    03/11/2026

@updated 06/30/2026

"""

import curses
from typing import TYPE_CHECKING, Iterator

from fuzzum.ui.help_popup import HelpPopup
from fuzzum.ui.panes.base_window import BaseWindow
from fuzzum.ui.panes.details_pane import DetailsPane
from fuzzum.ui.panes.preview_pane import PreviewPane
from fuzzum.ui.panes.results_pane import ResultsPane
from fuzzum.ui.panes.search_pane import SearchPane

if TYPE_CHECKING:
    from fruzzum.app import App


class WindowManager:
    def __init__(self, app: "App"):
        self.app = app

        self.details = DetailsPane(app)
        self.previews = PreviewPane(app)
        self.results = ResultsPane(app)
        self.search = SearchPane(app)

        self.details.visible = self.app.config.get("panes", "details") or False

        self.previews.visible = (
            self.app.config.get("panes", "preview") or False
        )

        self.window_list = [
            self.results,
            self.previews,
            self.search,
            self.details,
        ]

        self.create()

    def __iter__(self) -> Iterator[BaseWindow]:
        yield from self.window_list

    @property
    def help(self) -> HelpPopup:
        return HelpPopup(self.app.stdscr)

    def toggle_window(self, window: BaseWindow) -> None:
        window.toggle_visibility()

        for pane in self:
            pane.needs_refresh = True

        self.resize()

    def create(self) -> None:
        for window in self:
            window.set_size()
            window.create()

    def refresh(self) -> None:
        for window in self:
            window.refresh_window()

        # Keep cursor in search pane.
        y, x = self.search.get_cursor_position()
        try:
            self.app.stdscr.move(y, x)
        except curses.error:
            pass

        curses.doupdate()

    def resize(self) -> None:
        for window in self:
            window.set_size()
            window.needs_refresh = True
