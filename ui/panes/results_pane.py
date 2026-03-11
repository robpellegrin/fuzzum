"""
@file    results_pane.py
@author  Rob Pellegrin
@date    03-11-2026

@updated 03-11-2026

"""

import curses
from pathlib import Path

from ui.base_window import BaseWindow


class ResultsPane(BaseWindow):
    """Scrollable results pane with highlight and vertical scrollbar."""

    def __init__(self, app, name):
        super().__init__(app, name)
        self.offset = 0  # top visible item
        self.cursor = 0  # selected item
        self.files = self.app.files

        self.show_filenames_only = self.app.config.get(
            "ui", "show_filenames_only") or False

        self.show_hidden_files = self.app.config.get(
            "ui", "show_hidden_files") or False

        self._filter_files()

    def create(self):
        self.win = curses.newwin(self.height - 3, self.width // 2, 0, 0)

    def header(self, results_count=0):
        self.win.addstr(
            0, 1, f" Results —— ({results_count:,d}) ", curses.color_pair(3)
        )

    def refresh(self):
        self.win.erase()
        self.win.box()
        self.header(len(self.files))

        self.h, self.w = self.win.getmaxyx()

        if not self.app.files:
            return

        self._draw_files()
        self._draw_scrollbar()
        self.win.noutrefresh()
        self.app.cursor = self.cursor

    def _filter_files(self) -> None:
        self.files = [
            Path(f).name if self.show_filenames_only else f
            for f in self.app.files
            if self.show_hidden_files or not self._is_hidden_path(f)
        ]

    def _is_hidden_path(self, path: str):
        return any(part.startswith(".") for part in path.split("/"))

    def toggle_filenames(self) -> None:
        self.show_filenames_only = not self.show_filenames_only
        self.app.config.set(
            self.show_filenames_only, "ui", "show_filenames_only"
        )
        self._filter_files()

    def toggle_hidden_files(self) -> None:
        self.show_hidden_files = not self.show_hidden_files
        self.app.config.set(self.show_hidden_files, "ui", "show_hidden_files")
        self._filter_files()

    def _draw_files(self):
        max_rows = self.h - 2
        # leave 1 col for scrollbar!
        max_width = self.w - 3

        visible = self.files[self.offset: self.offset + max_rows]

        for i, file in enumerate(visible):
            row = i + 1
            text = file[:max_width]

            try:
                if self.offset + i == self.cursor:
                    self.win.addstr(row, 1, text, curses.A_REVERSE)
                else:
                    self.win.addstr(row, 1, text)
            except curses.error:
                pass

    def _draw_scrollbar(self):
        max_rows = self.h - 2

        # draw vertical scrollbar if needed
        total_items = len(self.app.files)
        if total_items > max_rows:
            scroll_height = max(1, int(max_rows * max_rows / total_items))
            scroll_start = int(self.offset * max_rows / total_items)
            for i in range(scroll_height):
                try:
                    self.win.addstr(1 + scroll_start, self.w - 2, "█")
                except curses.error:
                    pass

    ##
    # Scrolling
    ##
    def move_down(self):
        if self.cursor < len(self.app.files) - 1:
            self.cursor += 1
        self._adjust_offset()

    def move_up(self):
        if self.cursor > 0:
            self.cursor -= 1
        self._adjust_offset()

    def page_down(self):
        page = self.win.getmaxyx()[0] - 2
        self.cursor = min(len(self.app.files) - 1, self.cursor + page)
        self._adjust_offset()

    def page_up(self):
        page = self.win.getmaxyx()[0] - 2
        self.cursor = max(0, self.cursor - page)
        self._adjust_offset()

    def go_top(self):
        self.cursor = 0
        self._adjust_offset()

    def go_bottom(self):
        self.cursor = len(self.app.files) - 1
        self._adjust_offset()

    def _adjust_offset(self):
        """Adjust the top-of-window offset to keep the cursor visible."""
        h = self.win.getmaxyx()[0] - 2
        if self.cursor < self.offset:
            self.offset = self.cursor
        elif self.cursor >= self.offset + h:
            self.offset = self.cursor - h + 1
