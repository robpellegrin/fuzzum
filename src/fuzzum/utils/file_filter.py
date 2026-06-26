"""
@file    file_filter.py
@author  Rob Pellegrin
@date    03-11-2026

@updated 03-16-2026

"""

import logging
from pathlib import Path
from typing import Optional, Union

from utils.config import Config

logger = logging.getLogger(__name__)


class FileFilter:
    def __init__(self, files: list[Path], config: Config):
        self._files: list[Path] = files
        self._filtered_files: list[Path] = files

        self.config = config

        self._show_hidden_files: bool = config.get(
            "file_filter", "show_hidden_files"
        )

        self._show_filename_only: bool = config.get(
            "file_filter", "show_filename_only"
        )

        self.filter()

    @property
    def files(self) -> list[Path]:
        return self._filtered_files

    @files.setter
    def files(self, files: list[Path]) -> None:
        self._files = files

    @property
    def show_hidden_files(self) -> bool:
        return self._show_hidden_files

    @show_hidden_files.setter
    def show_hidden_files(self, new_state: bool) -> None:
        self._show_hidden_files = new_state
        self.filter()

        self.config.set(new_state, "file_filter", "show_hidden_files")

    @property
    def show_filename_only(self) -> bool:
        return self._show_filename_only

    @show_filename_only.setter
    def show_filename_only(self, new_state: bool) -> None:
        self._show_filename_only = new_state
        self.filter()

        self.config.set(new_state, "file_filter", "show_filename_only")

    def _is_hidden_file(self, path: Path) -> bool:
        return any(part.startswith(".") for part in Path(path).parts)

    def filter(self, filter_pattern: Optional[str] = None) -> None:
        filtered_files: list[Path] = []

        for f in self._files:
            # Skip hidden files.
            if not self.show_hidden_files and self._is_hidden_file(f):
                continue

            # Skip files that don't contain pattern.
            if filter_pattern and filter_pattern in f.parts:
                continue

            filtered_files.append(f)

        self._filtered_files = filtered_files

    def __getitem__(self, index: Union[int, Path]) -> Union[Path, list[Path]]:
        # Check if the index is a slice
        if isinstance(index, slice):
            return self.files[index]

        # Handle single index access
        if isinstance(index, int):
            # Handle negative indexing
            return self.files[index % len(self.files)]

        raise IndexError("Index out of range")

    def __len__(self) -> int:
        return len(self.files)
