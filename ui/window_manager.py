"""
@file    window_manager.py
@author  Rob Pellegrin
@date    03-11-2026

@updated 03-11-2026

"""

from ui.panes.details_pane import DetailsPane
from ui.panes.preview_pane import PreviewPane
from ui.panes.results_pane import ResultsPane
from ui.panes.search_pane import SearchPane
from ui.help_popup import HelpPopup


class WindowManager:
    def __init__(self, app):
        self.app = app

        self.results = ResultsPane(app, "results")
        self.previews = PreviewPane(app, "preview")
        self.search = SearchPane(app, "search")
        self.details = DetailsPane(app, "details")

        self.right_pane = [
            self.results,
            self.search,
        ]

        self.left_pane = [
            self.previews,
            self.details,
        ]

    @property
    def help(self):
        return HelpPopup(self.app.stdscr)

    def toggle_window(self, window):
        window.toggle()

        window.win.clear()
        window.win.refresh()

        self.resize()

    def create(self):
        for window in self.right_pane:
            window.create()

        for window in self.left_pane:
            window.create()

    def refresh(self):
        self.resize()

        for window in self.right_pane:
            if window.visible is True:
                window.refresh()

        for window in self.left_pane:
            if window.visible is True:
                window.refresh()

    def resize(self):
        height, width = self.app.stdscr.getmaxyx()

        if self.previews.visible is not True:
            self.results.resize(height - 3, width)
        else:
            self.results.resize(height - 3, width // 2)

        if self.details.visible is not True:
            self.search.resize(3, width)
        else:
            self.search.resize(3, width // 2)

        for window in self.right_pane:
            if not window.visible:
                window.win.erase()

        for window in self.left_pane:
            if not window.visible:
                window.win.erase()
