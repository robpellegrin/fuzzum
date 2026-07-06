"""
@file    preview_pane.py
@author  Rob Pellegrin
@date    03/11/2026

@updated 06/25/2026

"""

import curses
import threading
from collections import OrderedDict
from pathlib import Path
from typing import TYPE_CHECKING

from fuzzum.ui.panes.base_window import BaseWindow
from fuzzum.ui.popups.message_popup import MessagePopup
from fuzzum.utils.curse_catcher import curse_catch

if TYPE_CHECKING:
    from fuzzum.app import App


class PreviewPane(BaseWindow):

    PREVIEW_LINES = 25
    MAX_PREVIEW_CACHE = 2_000

    TEXT_EXTENSIONS = {
        ".txt",
        ".py",
        ".md",
        ".json",
        ".yaml",
        ".yml",
        ".csv",
        ".xml",
        ".html",
        ".css",
        ".js",
    }

    def __init__(self, app: "App") -> None:
        super().__init__(app)

        self._preview_cache: OrderedDict[Path, list[str]] = OrderedDict()
        self._preview_lock = threading.Lock()

        self.set_size()

    def set_size(self) -> None:
        height, width = self.win.getmaxyx()

        self.height = height - 3
        self.width = width // 2

    @curse_catch
    def create(self) -> None:
        left_width = self.width
        right_width = self.width - left_width

        self.win = curses.newwin(self.height, right_width, 0, left_width)

    @curse_catch
    def draw(self) -> None:
        super().draw()

        self.win.addstr(0, 2, "Preview", curses.color_pair(3))
        self._draw_preview()

    def _read_preview(
        self, path: Path, max_lines: int = PREVIEW_LINES
    ) -> list[str]:
        """Read text preview of a file"""

        if not self._is_text_file(path):
            return ["Binary cannot be previewed"]

        lines: list[str] = []

        try:
            with open(path, "r", errors="replace", encoding="UTF-8") as f:
                for i, line in enumerate(f):
                    if i >= max_lines:
                        break

                    lines.append(self.sanitize(line))

        except (FileNotFoundError, PermissionError) as e:
            lines = [f"Error reading file: {e}"]

        return lines

    def _is_text_file(self, path: Path) -> bool:
        if path.suffix in self.TEXT_EXTENSIONS:
            return True

        try:
            with open(path, "rb") as f:
                chunk = f.read(8_000)
                return b"\0" not in chunk
        except (FileNotFoundError, PermissionError):
            return False

    def _load_preview_async(self, path: Path) -> None:
        """Thread function to read preview and store in cache"""

        try:
            lines: list[str] = self._read_preview(path)
            with self._preview_lock:
                self._preview_cache[path] = lines
                self._preview_cache.move_to_end(path)

                # Check if cache is full. Remove LRU if true.
                if len(self._preview_cache) > self.MAX_PREVIEW_CACHE:
                    self._preview_cache.popitem(last=False)

        except (PermissionError, FileNotFoundError):
            with self._preview_lock:
                self._preview_cache[path] = ["Error reading preview"]

    @curse_catch
    def _draw_preview(self) -> None:
        max_lines: int = self.height
        max_width: int = self.width - 4

        if not (selected_file := self.app.files[self.app.cursor]):
            MessagePopup(self).show_message("Nothing to preview.")
            return

        if not self._is_text_file(selected_file):
            MessagePopup(self).show_message("Binary cannot be previewed.")
            return

        lines: list[str] = self._read_preview(selected_file, max_lines)

        if not lines:
            MessagePopup(self).show_message("EMPTY FILE")
            return

        for row, line in enumerate(lines[:max_lines], start=1):
            # Start printing two cols to the right of box around pane.
            col = 2

            self.win.addnstr(row, col, line.rstrip(), max_width)

    def sanitize(self, line: str) -> str:
        """Returns a string of only ASCII characters and newlines."""

        sanitized_line = ""

        for ch in line:
            if 32 <= ord(ch) <= 126:
                sanitized_line += ch

            if ch == "\n":
                sanitized_line += ch

        return sanitized_line
