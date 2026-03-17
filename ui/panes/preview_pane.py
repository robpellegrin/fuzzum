"""
@file    preview_pane.py
@author  Rob Pellegrin
@date    03-11-2026

@updated 03-16-2026

"""

import curses
import logging
import threading
from collections import OrderedDict
from pathlib import Path
from typing import TYPE_CHECKING

from ui.base_window import BaseWindow
from ui.popups.message_popup import MessagePopup

if TYPE_CHECKING:
    from app.app import App

logger = logging.getLogger(__name__)


class PreviewPane(BaseWindow):

    PREVIEW_LINES = 100
    MAX_PREVIEW_CACHE = 2_000

    TEXT_EXTENSIONS = {
        ".txt", ".py", ".md", ".json", ".yaml", ".yml",
        ".csv", ".xml", ".html", ".css", ".js"
    }

    def __init__(self, app: "App", name: str) -> None:
        super().__init__(app, name)

        self._preview_cache = OrderedDict()
        self._preview_lock = threading.Lock()

    def create(self) -> None:
        left_width = self.width // 2
        right_width = self.width - left_width

        self.win = curses.newwin(self.height - 3, right_width, 0, left_width)

    def draw(self) -> None:
        self.win.erase()
        self.win.box()
        self.win.addstr(0, 2, " Preview ", curses.color_pair(3))

        self._draw_preview()

    def _read_preview(self, path, max_lines=PREVIEW_LINES):
        """Read text preview of a file"""

        if not self._is_text_file(path):
            return ["Binary cannot be previewed"]

        lines = []

        try:
            with open(path, "r", errors="replace", encoding="UTF-8") as f:
                for i, line in enumerate(f):
                    if i >= max_lines:
                        return lines

                    lines.append(line.rstrip())
        except (FileNotFoundError, PermissionError) as e:
            lines = [f"Error reading file: {e}"]

        return lines

    def _is_text_file(self, path: Path) -> bool:
        if path.suffix.lower() in self.TEXT_EXTENSIONS:
            return True

        try:
            with open(path, "rb") as f:
                chunk = f.read(8_000)
                return b"\0" not in chunk
        except (FileNotFoundError, PermissionError):
            return False

    def _load_preview_async(self, path):
        """Thread function to read preview and store in cache"""

        try:
            lines = self.read_preview(path)
            with self._preview_lock:
                self._preview_cache[path] = lines
                self._preview_cache.move_to_end(path)

                # Check if cache is full. Remove LRU if true.
                if len(self._preview_cache) > self.MAX_PREVIEW_CACHE:
                    self._preview_cache.popitem(last=False)
                    logging.info("Cache is full. Popping LRU")

        except Exception:
            with self._preview_lock:
                self._preview_cache[path] = ["Error reading preview"]

    def _draw_preview(self) -> None:
        max_lines: int = self.height - 3
        max_width: int = self.width - 6

        selected_file: Path = self.app.wm.results.get_selected_file()

        lines: list[str] = self._read_preview(selected_file, 100)

        if not lines:
            MessagePopup(self).show_message(" File is empty!")
            return

        for i, line in enumerate(lines[:max_lines]):
            line = line.strip()
            row: int = i + 1

            try:
                self.win.addstr(row, 2, line[:max_width])
            except curses.error as e:
                logging.error("_draw_preview: %s", e)
