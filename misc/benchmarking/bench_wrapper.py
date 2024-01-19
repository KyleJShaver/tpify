from time import perf_counter
from timeit import timeit
from typing import Callable

from tpify import TPResponse, TPResult, tp, tpify, tpify_function, tpify_result

FIB_NUM = 13
TIMEIT_ITERATIONS = 50_000
WARMUP_ITERATIONS = int(TIMEIT_ITERATIONS / 2)


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


fibonacci_named_tp: Callable = tpify_function(fibonacci)


@tpify_result
def fibonacci_result_tp(n: int = FIB_NUM) -> int:
    if n < 0:
        raise ValueError("Cannot compute Fibonacci number less than 0")
    if n == 0:
        return 0
    if 1 <= n <= 2:
        return 1
    return fibonacci_result_tp(n - 1).ok + fibonacci_result_tp(n - 2).ok


fibonacci_result_named_tp: Callable = tpify_result(fibonacci)


if __name__ == "__main__":
    warmup_start = perf_counter()
    print("Warming up interpreter...")
    timeit(fibonacci, number=WARMUP_ITERATIONS)
    timeit(fibonacci_tp, number=WARMUP_ITERATIONS)
    timeit(fibonacci_named_tp, number=WARMUP_ITERATIONS)
    timeit(fibonacci_result_tp, number=WARMUP_ITERATIONS)
    timeit(fibonacci_result_named_tp, number=WARMUP_ITERATIONS)
    print(f"Interpreter is warmed after {perf_counter() -warmup_start:.2f} seconds")

    fibonacci_time = timeit(fibonacci, number=TIMEIT_ITERATIONS)
    print(f"Base `fibonacci({FIB_NUM})` completed after {fibonacci_time:.2f} seconds")

    fibonacci_tp_time = timeit(fibonacci_tp, number=TIMEIT_ITERATIONS)
    print(
        f"{int((fibonacci_tp_time-fibonacci_time)/fibonacci_time*1000)/10.0}% slowdown using tpify"
    )

    fibonacci_tp_named_time = timeit(fibonacci_named_tp, number=TIMEIT_ITERATIONS)
    print(
        f"{int((fibonacci_tp_named_time-fibonacci_time)/fibonacci_time*1000)/10.0}% slowdown using tpify named"
    )

    fibonacci_result_tp_time = timeit(fibonacci_result_tp, number=TIMEIT_ITERATIONS)
    print(
        f"{int((fibonacci_result_tp_time-fibonacci_time)/fibonacci_time*1000)/10.0}% slowdown using tpify_result"
    )

    fibonacci_result_named_tp_time = timeit(
        fibonacci_result_named_tp, number=TIMEIT_ITERATIONS
    )
    print(
        f"{int((fibonacci_result_named_tp_time-fibonacci_time)/fibonacci_time*1000)/10.0}% slowdown using tpify_result named"
    )
