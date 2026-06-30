"""
@file    main.py
@author  Rob Pellegrin
@date    03/11/2026


TODO:
    - Add '--levels' flag to set depth limit.
    - Add argparse for CLI args to call
        `find .  -type f -name *.py | xargs -P 10 grep "Rob"`.


@updated 06/25/2026

"""

import curses
import logging
import os
from functools import partial

from fuzzum.app.app import App
from fuzzum.app.cli import init_cli_args

# Enable logging
logging.basicConfig(
    filename="app.log",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def main(stdscr: curses.window, args) -> None:
    stdscr.nodelay(True)
    stdscr.timeout(50)

    curses.curs_set(1)
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_YELLOW, -1)

    app = App(stdscr, args)

    try:
        result = app.run()
    except KeyboardInterrupt:
        pass

    return result


def cli() -> None:
    """Helper function to call main when using as package."""

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
