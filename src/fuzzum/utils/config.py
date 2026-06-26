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

    CONFIG_DIR = Path.home()
    CONFIG_FILE = CONFIG_DIR / ".fuzzum_config"

    def __init__(self) -> None:
        self.data: dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        # Defaults
        self.data = {
            "panes": {
                "preview": True,
                "details": True
            },
            "file_filter": {
                "show_hidden_files": True,
                "show_filename_only": False
            }
        }

        if not self.CONFIG_FILE.exists():
            return

        try:
            with open(self.CONFIG_FILE, encoding="UTF-8") as f:
                self.data.update(json.load(f))
        except json.JSONDecodeError:
            logger.warning("Config file is corrupt!")

    def save(self) -> None:
        dbug("Config saved")
        self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        with open(self.CONFIG_FILE, "w", encoding="UTF-8") as f:
            json.dump(self.data, f, indent=4)

    def get(self, *keys: str) -> Any:
        value: Any = self.data

        for k in keys:
            value = value[k]

        return value

    def set(self, value: Any, *keys: str) -> None:
        d: dict[str, Any] = self.data

        for k in keys[:-1]:
            d = d.setdefault(k, {})

        d[keys[-1]] = value
