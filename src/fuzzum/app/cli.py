import argparse
from os import getcwd
from pathlib import Path


def init_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="fuzz", description="A custom fuzzy file finder."
    )

    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=getcwd(),
        help="Root path to search",
    )

    parser.add_argument(
        "--depth",
        default=0,
        type=int,
        help="Maximum number of sub directories to search (default=0).",
    )

    return parser.parse_args()
