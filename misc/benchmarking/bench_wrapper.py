from functools import cache
from time import perf_counter
from timeit import timeit
from typing import Callable, Tuple

from tpify import TPResponse, tp, tpify, tpify_function

FIB_NUM = 13
TIMEIT_ITERATIONS = 10_000


def fibonacci(n: int = FIB_NUM) -> int:
    if n < 0:
        raise ValueError("Cannot compute Fibonacci number less than 0")
    if n == 0:
        return 0
    if 1 <= n <= 2:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


@tpify()
def fibonacci_tp(n: int = FIB_NUM) -> TPResponse:
    if n < 0:
        return (
            tp.InputError,
            ValueError("Cannot compute Fibonacci number less than 0"),
        )
    if n == 0:
        return (
            tp.OK,
            0,
        )
    if 1 <= n <= 2:
        return (
            tp.OK,
            1,
        )
    return fibonacci_tp(n - 1).content + fibonacci_tp(n - 2).content


fibonacci_tp_named = tpify_function(fibonacci)

if __name__ == "__main__":
    fibonacci_time = timeit(fibonacci, number=TIMEIT_ITERATIONS)
    fibonacci_tp_time = timeit(fibonacci_tp, number=TIMEIT_ITERATIONS)
    fibonacci_tp_named_time = timeit(fibonacci_tp_named, number=TIMEIT_ITERATIONS)
    print(
        f"{int((fibonacci_tp_time-fibonacci_time)/fibonacci_time*1000)/10.0}% slowdown using tpify"
    )
    print(
        f"{int((fibonacci_tp_named_time-fibonacci_time)/fibonacci_time*1000)/10.0}% slowdown using tpify named"
    )
