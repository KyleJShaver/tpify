from time import perf_counter
from typing import Callable

from tpify.core.response import Response, StatusResponse


def tpify(func: Callable):
    def tpified_function(*args, **kwargs):
        start = perf_counter()
        resp = Response(func=func, args=args, kwargs=kwargs)
        try:
            result = func(*args, **kwargs)
            if type(result) not in (
                Response,
                StatusResponse,
            ):
                resp.content = result
                resp.status_code = 200
            elif isinstance(result, StatusResponse):
                resp.content = result.content
                resp.status_code = result.status_code
            else:
                return result
        except Exception as e:
            resp.content = e
            resp.status_code = 500
        resp.elapsed = perf_counter() - start
        return resp

    return tpified_function
