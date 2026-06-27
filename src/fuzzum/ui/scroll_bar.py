"""
@file    scroll_bar.py
@author  Rob Pellegrin
@date    06/27/2026

@updated 06/27/2026

"""

import curses


class ScrollBar:

    def __init__(
        self,
        win: curses.window,
        height: int,
        width: int,
        total_rows: int,
        offset: int,
    ) -> None:
        self.win = win
        self.visible_rows = height
        self.total_rows = total_rows
        self.width = width
        self.offset = offset

    def draw(self) -> None:
        # Don't draw if all rows are visible.
        if self.total_rows <= self.visible_rows:
            return

        # Thumb size proportional to visible content.
        thumb_size = max(
            1, int(self.visible_rows * (self.visible_rows / self.total_rows))
        )

        max_offset: int = self.total_rows - self.visible_rows

        thumb_pos = int(
            (self.offset / max_offset) * (self.visible_rows - thumb_size)
        )

        for i in range(self.visible_rows):
            char = "│"

            if thumb_pos <= i < thumb_pos + thumb_size:
                char = "█"

            try:
                self.win.addstr(i + 1, self.width, char)
            except curses.error:
                pass
