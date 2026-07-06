import curses


def curse_catch(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except curses.error:
            pass
        return result

    return wrapper
