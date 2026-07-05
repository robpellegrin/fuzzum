"""
@file    scroll_bar.py
@author  Rob Pellegrin
@date    06/27/2026

@updated 06/27/2026

"""

import curses


class ScrollBar:

    def __init__(
        self, win: curses.window, total_rows: int, offset: int
    ) -> None:
        self.win = win
        self.height: int
        self.width: int

        self.height, self.width = self.win.getmaxyx()

        # Adjust height and width to create room for scroll bar.
        self.height -= 2
        self.width -= 2

        self.total_rows = total_rows
        self.offset = offset

    def draw(self) -> None:
        # Don't draw if all rows are visible.
        if self.total_rows <= self.height:
            return

        # Thumb size proportional to visible content.
        thumb_size = max(1, int(self.height * (self.height / self.total_rows)))

        max_offset: int = self.total_rows - self.height

        thumb_pos = int(
            (self.offset / max_offset) * (self.height - thumb_size)
        )

        for i in range(self.height):
            char = "│"

            if thumb_pos <= i < thumb_pos + thumb_size:
                char = "█"

            try:
                self.win.addstr(i + 1, self.width, char)
            except curses.error:
                pass
