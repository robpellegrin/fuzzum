"""
@file    main.py
@author  Rob Pellegrin
@date    03-11-2026

@updated 03-13-2026

"""

import logging
import curses

from app.app import App

# Enable logging
logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def main(stdscr: curses.window) -> None:
    stdscr.nodelay(True)
    stdscr.timeout(50)

    curses.curs_set(1)
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_YELLOW, -1)

    app = App(stdscr)

    try:
        app.run()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    curses.wrapper(main)
