"""
@file    main.py
@author  Rob Pellegrin
@date    03-11-2026

@updated 03-11-2026

"""

import curses

from app.app import App


def main(stdscr):
    app = App(stdscr)
    try:
        app.run()
    except KeyboardInterrupt:
        pass

    # Reset terminal on exit
    print("\033c")


if __name__ == "__main__":
    curses.wrapper(main)
