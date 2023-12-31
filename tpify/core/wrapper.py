from typing import Callable

from tpify.core.request import tpify_function


def tpify(func: Callable):
    def tpified_function(*args, **kwargs):
        return tpify_function(func, *args, **kwargs)

    return tpified_function
