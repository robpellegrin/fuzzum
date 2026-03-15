"""
@file    window_manager.py
@author  Rob Pellegrin
@date    03-11-2026

@updated 03-14-2026

"""

import logging
import sys
from typing import TYPE_CHECKING

from ui.base_window import BaseWindow
from ui.help_popup import HelpPopup
from ui.panes.details_pane import DetailsPane
from ui.panes.preview_pane import PreviewPane
from ui.panes.results_pane import ResultsPane
from ui.panes.search_pane import SearchPane

if TYPE_CHECKING:
    from app.app import App

logger = logging.getLogger(__name__)


class WindowManager:
    def __init__(self, app: "App"):
        self.app = app

        self.details = DetailsPane(app, "details")
        self.previews = PreviewPane(app, "preview")
        self.results = ResultsPane(app, "results")
        self.search = SearchPane(app, "search")

        self.window_list = [
            self.details,
            self.previews,
            self.results,
            self.search,
        ]

    def __iter__(self) -> list[BaseWindow]:
        for window in self.window_list:
            yield window

    @property
    def help(self) -> HelpPopup:
        return HelpPopup(self.app.stdscr)

    def toggle_window(self, window: BaseWindow) -> None:
        window.toggle_visibility()

        for window in self:
            window.needs_refresh = True

    def create(self) -> None:
        for window in self:
            window.create()

        self.resize()

    def refresh(self) -> None:
        for window in self:
            window.refresh()

        y, x = self.search.get_cursor_position()
        self.app.stdscr.move(y, x)

    def resize(self) -> None:
        height, width = self.app.stdscr.getmaxyx()

        if not self.previews.visible:
            self.results.resize(height - 3, width)
        else:
            self.results.resize(height - 3, width // 2)

        if not self.details.visible:
            self.search.resize(3, width)
        else:
            self.search.resize(3, width // 2)
