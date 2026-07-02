"""
@file    file_filter.py
@author  Rob Pellegrin
@date    03/11/2026

@updated 06/25/2026

"""

import logging
from pathlib import Path
from typing import Union

logger = logging.getLogger(__name__)


class FileFilter:
    def __init__(self, files: list[Path]):
        self._all_files = files
        self._filtered_files: list[Path] = files

    @property
    def files(self) -> list[Path]:
        return self._filtered_files

    def _is_hidden_file(self, path: Path) -> bool:
        return any(part.startswith(".") for part in Path(path).parts)

    def filter(self, filter_pattern: str) -> None:
        filtered_files: list[Path] = []

        for file in self._all_files:
            if filter_pattern in file.name:
                filtered_files.append(file)

        self._filtered_files = filtered_files

    def __getitem__(self, index: Union[int, slice]) -> Path:
        # Prevent indexing an empty list.
        if not self._filtered_files:
            return self._filtered_files

        # Check if the index is a slice.
        if isinstance(index, slice):
            return self._filtered_files[index]

        # Handle single index access.
        if isinstance(index, int):
            # Handle negative indexing
            return self._filtered_files[index % len(self._filtered_files)]

        raise IndexError("Index out of range")

    def __len__(self) -> int:
        return len(self._filtered_files)
