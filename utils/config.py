"""
@file    config.py
@author  Rob Pellegrin
@date    03-11-2026

@updated 03-14-2026

"""

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)
dbug = logger.debug


class Config:

    CONFIG_DIR = Path.home() / ".config" / "myapp"
    CONFIG_FILE = CONFIG_DIR / "config.json"

    def __init__(self) -> None:
        self.data = {
            "panes": {"preview": False, "details": True},
            "ui": {"show_hidden_files": True, "show_filenames_only": False},
        }

        self.load()

    def load(self) -> None:
        """
        Loads the contents of the config file.

        """

        dbug("Config loaded")

        if self.CONFIG_FILE.exists():
            with open(self.CONFIG_FILE, encoding="UTF-8") as f:
                self.data.update(json.load(f))

    def save(self) -> None:
        """
        Writes the state of self.data to config file.

        """

        dbug("Config saved")
        self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        with open(self.CONFIG_FILE, "w", encoding="UTF-8") as f:
            json.dump(self.data, f, indent=4)

    def get(self, *keys: str) -> Any:
        """
        Returns the value corresponding to the supplied key.

        """

        value: Any = self.data

        for k in keys:
            value = value[k]

        return value

    def set(self, value: Any, *keys: str) -> None:
        """
        Updates a config value, then writes the new state to config
        file.

        """

        d: dict[str, Any] = self.data

        for k in keys[:-1]:
            d = d.setdefault(k, {})

        d[keys[-1]] = value
