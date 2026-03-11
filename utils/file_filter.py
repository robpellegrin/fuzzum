"""
@file    file_filter.py
@author  Rob Pellegrin
@date    03-11-2026

@updated 03-11-2026

"""

from pathlib import Path


class FileFilter:
    def __init__(self, show_hidden=False, pattern=None):
        self.show_hidden = show_hidden
        self.pattern = pattern

    def is_hidden(self, path):
        return any(part.startswith(".") for part in Path(path).parts)

    def filter(self, files):
        result = []
        for f in files:
            if not self.show_hidden and self.is_hidden(f):
                continue
            if self.pattern and not Path(f).match(self.pattern):
                continue
            result.append(f)
        return result
