import curses
import functools
from typing import Any, Callable, Optional, TypeVar

R = TypeVar("R")


def curse_catch(func: Callable[..., R]) -> Callable[..., Optional[R]]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Optional[R]:
        try:
            return func(*args, **kwargs)
        except curses.error:
            return None

    return wrapper
