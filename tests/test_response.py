from time import perf_counter

from tests.utils import double_number
from tpify import Response, StatusResponse, tpify


class TestCoreFunction:
    def test_tpified_response(_):
        def double_number_tpified_response(n: int):
            start = perf_counter()
            resp = double_number(n)
            return Response(
                double_number_tpified_response,
                (n,),
                None,
                200,
                resp,
                {},
                perf_counter() - start,
            )

        arg_val = (2,)
        resp = double_number_tpified_response(*arg_val)
        assert isinstance(resp, Response)
        assert resp.content == double_number(*arg_val)
        assert resp.status_code == 200
        assert str(resp) == "<Response [200]>"

    def test_tpified_status_response(_):
        def doble_number_tpified_status_response(n: int):
            return StatusResponse(200, double_number(n))

        arg_val = (2,)
        resp = doble_number_tpified_status_response(*arg_val)
        assert isinstance(resp, StatusResponse)
        assert resp.content == double_number(*arg_val)
        assert resp.status_code == 200
        assert str(resp) == "<StatusResponse [200]>"

    def test_double_number_decorator(_):
        @tpify
        def double_number_decorator(n: int):
            return double_number(n)

        arg_val = (2,)
        resp = double_number_decorator(*arg_val)
        assert isinstance(resp, Response)
        assert resp.content == double_number(*arg_val)
        assert resp.status_code == 200

    def test_double_number_tpified_response_decorator(_):
        @tpify
        def double_number_tpified_response_decorator(n: int):
            start = perf_counter()
            resp = double_number(n)
            return Response(
                double_number_tpified_response_decorator,
                (n,),
                None,
                200,
                resp,
                {},
                perf_counter() - start,
            )

        arg_val = (2,)
        resp = double_number_tpified_response_decorator(*arg_val)
        assert isinstance(resp, Response)
        assert resp.content == double_number(*arg_val)
        assert resp.status_code == 200

    def test_doble_number_tpified_status_response_decorator(_):
        @tpify
        def doble_number_tpified_status_response_decorator(n: int):
            return StatusResponse(200, double_number(n))

        arg_val = (2,)
        resp = doble_number_tpified_status_response_decorator(*arg_val)
        assert isinstance(resp, Response)
        assert resp.content == double_number(*arg_val)
        assert resp.status_code == 200
        print(resp.func.__name__)


class TestExceptions:
    def test_raise_exception_default_500(_):
        @tpify
        def raise_exception():
            raise Exception("This could be any exception in a function")

        resp = raise_exception()
        assert resp.status_code == 500
        assert isinstance(resp.content, Exception)

    def test_raise_exception_status_response(_):
        @tpify
        def raise_exception():
            return StatusResponse(403, ValueError("You're not allowed to do that"))

        resp = raise_exception()
        assert resp.status_code == 403
        assert isinstance(resp.content, ValueError)
