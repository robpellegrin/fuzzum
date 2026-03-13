"""
@file    help_popup.py
@author  Rob Pellegrin
@date    03-11-2026

@updated 03-11-2026

"""

import curses


class HelpPopup:
    def __init__(self, stdscr):
        self.stdscr = stdscr

    def show(self):
        height, width = self.stdscr.getmaxyx()

        sh, sw = self.stdscr.getmaxyx()

        win_h = 15
        win_w = 50

        start_y = (sh - win_h) // 2
        start_x = (sw - win_w) // 2

        shadow = curses.newwin(win_h, win_w, start_y + 1, start_x + 2)

        win = curses.newwin(win_h, win_w, start_y, start_x)
        win.box()

        help_text = [
            "",
            "\tq\tQuit",
            "\t?\tShow help",
            "",
            "\tCtrl+P\tToggle preview pane",
            "\tCtrl+D\tToggle details pane",
            "",
            "\t.     \tShow/Hide hidden files",
            "\t>     \tToggle display path/filename",
            "",
            "",
            "\tPress any key to close",
        ]

        win.addstr(0, 2, " Help ", curses.A_BOLD)
        for i, line in enumerate(help_text):
            win.addstr(1 + i, 3, line)

        shadow.noutrefresh()
        win.noutrefresh()
        curses.doupdate()

        win.getch()  # wait for key press
