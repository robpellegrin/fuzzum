"""
@file:    cli.py
@author:  Rob Pellegrin
@date:    06/30/2026

Handles initialization and parsing of CLI arguments.

@updated: 07/04/2026

"""

import argparse
from os import getcwd
from pathlib import Path


def init_cli_args() -> argparse.Namespace:
    """Parse and return the command-line arguments for the application.

    Configures the command-line interface for the fuzzy file finder and parses
    the arguments supplied by the user.

    Supported arguments:
        path: Optional root directory to search. Defaults to the current
            working directory if omitted.
        --depth: Maximum directory depth to traverse relative to the root
            search directory. A default value of `0` limits searching to the
            root directory only.

    Returns:
        An `argparse.Namespace` containing the parsed command-line arguments.
    """

    parser = argparse.ArgumentParser(
        prog="fuzz", description="A custom fuzzy file finder."
    )

    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=getcwd(),
        help="Directory to search.",
    )

    parser.add_argument(
        "--depth",
        default=0,
        type=int,
        help="Maximum number of sub directories to search (default=0).",
    )

    return parser.parse_args()
