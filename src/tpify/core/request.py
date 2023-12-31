from time import perf_counter
from typing import Callable

from tpify.core.response import Response, StatusResponse


def tpify_function(func: Callable, *args, **kwargs) -> Response:
    start = perf_counter()
    resp = Response(func=func, args=args, kwargs=kwargs)
    try:
        result = func(*args, **kwargs)
        if isinstance(result, Response):
            return result
        elif isinstance(result, StatusResponse):
            resp.content = result.content
            resp.status_code = result.status_code
        else:
            resp.content = result
            resp.status_code = 200
    except Exception as e:
        resp.content = e
        resp.status_code = 500
    resp.elapsed = perf_counter() - start
    return resp
