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
import sys


class WindowManager:
    def __init__(self, app):
        self.app = app

        self.results = ResultsPane(app, "results")
        self.previews = PreviewPane(app, "preview")
        self.search = SearchPane(app, "search")
        self.details = DetailsPane(app, "details")

        self.right_pane = [
            self.previews,
            self.details,
        ]

        self.left_pane = [
            self.results,
            self.search,
        ]

    @property
    def help(self):
        return HelpPopup(self.app.stdscr)

    def toggle_window(self, window):
        window.toggle()

        for left, right in zip(self.right_pane, self.left_pane):
            left.needs_refresh = True
            right.needs_refresh = True

    def create(self):
        for window in self.right_pane:
            window.create()

        for window in self.left_pane:
            window.create()

        self.resize()

    def refresh(self):
        for left, right in zip(self.left_pane, self.right_pane):
            left.refresh()
            right.refresh()

        y, x = self.search.get_cursor_position()
        self.app.stdscr.move(y, x)

    def resize(self):
        height, width = self.app.stdscr.getmaxyx()

        if not self.previews.visible:
            print("PREVIEWS DISABLED", file=sys.stderr)
            self.results.resize(height - 3, width)
        else:
            self.results.resize(height - 3, width // 2)

        if not self.details.visible:
            self.search.resize(3, width)
        else:
            self.search.resize(3, width // 2)

#        self.app.stdscr.erase()
        #self.refresh()

#        for window in self.right_pane:
#            if not window.visible:
#                window.win.erase()
#
#        for window in self.left_pane:
#            if not window.visible:
#                window.win.erase()
