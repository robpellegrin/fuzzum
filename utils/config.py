"""
@file    config.py
@author  Rob Pellegrin
@date    03-11-2026

@updated 03-11-2026

"""

import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "myapp"
CONFIG_FILE = CONFIG_DIR / "config.json"


class Config:
    def __init__(self):
        self.data = {
          "panes": {
            "preview": False,
            "details": True
          },
          "ui": {
            "show_hidden_files": True,
            "show_filenames_only": False
          }
        }

        self.load()

    def load(self):
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE) as f:
                self.data.update(json.load(f))

    def save(self):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.data, f, indent=4)

    def get(self, *keys):
        value = self.data
        for k in keys:
            value = value[k]
        return value

    def set(self, value, *keys):
        d = self.data
        for k in keys[:-1]:
            d = d.setdefault(k, {})
        d[keys[-1]] = value
        self.save()
