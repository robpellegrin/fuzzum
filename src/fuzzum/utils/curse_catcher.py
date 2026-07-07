import curses
import functools


def curse_catch(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except curses.error:
            return None

    return wrapper
