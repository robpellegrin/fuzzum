"""
@file    file_filter.py
@author  Rob Pellegrin
@date    03-11-2026

@updated 03-15-2026

"""

from pathlib import Path


class FileFilter:
    def __init__(self, files: list[Path], show_hidden=False, pattern=None):
        self.files = files

        self.show_hidden = show_hidden
        self.pattern = pattern

    @property
    def files(self) -> list[Path]:
        return self._files

    @files.setter
    def files(self, files: list[Path]) -> None:
        self._files = files

    def toggle_hidden(self) -> bool:
        self.show_hidden = not self.show_hidden

        return self.show_hidden

    def _is_hidden(self, path):
        return any(part.startswith(".") for part in Path(path).parts)

    def filter(self, files):
        result = []

        for f in files:
            if not self.show_hidden and self._is_hidden(f):
                continue
            if self.pattern and not Path(f).match(self.pattern):
                continue
            result.append(f)

        return result

    def __getitem__(self, index: int) -> Path:
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
