"""
@file    main.py
@author  Rob Pellegrin
@date    03/11/2026

Main entry point for Fuzzum.

@updated 06/25/2026

"""

import argparse
import curses
import os
from functools import partial
from pathlib import Path
from typing import Any

from fuzzum.app import App
from fuzzum.cli import init_cli_args


def main(stdscr: curses.window, args: argparse.Namespace) -> Any:
    """Initialize the curses environment and run the application.

    Configures the curses terminal, including input handling, cursor
    visibility, color support, and color pairs. After initialization,
    constructs the application and enters its main event loop.

    Args:
        stdscr: The curses standard screen window provided by `curses.wrapper`.
        args: Parsed command-line arguments.

    Returns:
        The value returned by `App.run`, which is expected to be a
        file system Path.

    """

    stdscr.nodelay(True)
    stdscr.timeout(50)

    curses.curs_set(1)
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_YELLOW, -1)
    curses.init_pair(10, curses.COLOR_RED, -1)

    app = App(stdscr, args)

    try:
        result: Path = app.run()
    except KeyboardInterrupt:
        return None

    return result


def cli() -> None:
    """Run the command-line interface.

    Parses command-line arguments, redirects standard output to the controlling
    terminal while the curses interface is active, and executes the
    application. After the curses session exits, restores the original
    standard output and prints the selected result, if any.

    """

    # Curses should write to tty instead of stdout.
    with open("/dev/tty", "w") as tty:
        old_stdout = os.dup(1)

        try:
            os.dup2(tty.fileno(), 1)
            result = curses.wrapper(partial(main, args=init_cli_args()))
        finally:
            os.dup2(old_stdout, 1)
            os.close(old_stdout)

    if result:
        print(result)
