from time import perf_counter

from tests.utils import double_number
from tpify import Response, StatusResponse, tpify


def test_httpized_response():
    def double_number_httpized_response(n: int):
        start = perf_counter()
        resp = double_number(n)
        return Response(
            double_number_httpized_response,
            (n,),
            None,
            200,
            resp,
            {},
            perf_counter() - start,
        )

    arg_val = (2,)
    resp = double_number_httpized_response(*arg_val)
    assert isinstance(resp, Response)
    assert resp.content == double_number(*arg_val)
    assert resp.status_code == 200


def test_httpized_status_response():
    def doble_number_httpized_status_response(n: int):
        return StatusResponse(200, double_number(n))

    arg_val = (2,)
    resp = doble_number_httpized_status_response(*arg_val)
    assert isinstance(resp, StatusResponse)
    assert resp.content == double_number(*arg_val)
    assert resp.status_code == 200


def test_double_number_decorator():
    @tpify
    def double_number_decorator(n: int):
        return double_number(n)

    arg_val = (2,)
    resp = double_number_decorator(*arg_val)
    assert isinstance(resp, Response)
    assert resp.content == double_number(*arg_val)
    assert resp.status_code == 200


def test_double_number_httpized_response_decorator():
    @tpify
    def double_number_httpized_response_decorator(n: int):
        start = perf_counter()
        resp = double_number(n)
        return Response(
            double_number_httpized_response_decorator,
            (n,),
            None,
            200,
            resp,
            {},
            perf_counter() - start,
        )

    arg_val = (2,)
    resp = double_number_httpized_response_decorator(*arg_val)
    assert isinstance(resp, Response)
    assert resp.content == double_number(*arg_val)
    assert resp.status_code == 200


def test_doble_number_httpized_status_response_decorator():
    @tpify
    def doble_number_httpized_status_response_decorator(n: int):
        return StatusResponse(200, double_number(n))

    arg_val = (2,)
    resp = doble_number_httpized_status_response_decorator(*arg_val)
    assert isinstance(resp, Response)
    assert resp.content == double_number(*arg_val)
    assert resp.status_code == 200
    print(resp.func.__name__)
