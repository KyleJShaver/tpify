import pytest
from tpify import TPResponse, tp, tpify, tpify_function
from tpify.core.wrapper import _DEFAULT_ERROR_CODE


def double_number(n: int) -> int:
    return n * 2


class TestCoreFunction:
    def test_double_number_pie_syntax(_):
        @tpify()
        def double_number_decorator(n: int):
            return double_number(n)

        arg_val = (2,)
        resp = double_number_decorator(*arg_val)
        assert isinstance(resp, tuple)
        assert isinstance(resp, TPResponse)
        assert resp.content == double_number(*arg_val)
        assert resp.status_code == tp.OK

    def test_double_number_named_function(_):
        double_tp = tpify_function(double_number)
        arg_val = (2,)
        resp = double_tp(*arg_val)
        assert isinstance(resp, tuple)
        assert isinstance(resp, TPResponse)
        assert resp.content == double_number(*arg_val)
        assert resp.status_code == tp.OK

    def test_too_many_tuple_vals(_):
        @tpify()
        def double_number_decorator(n: int):
            return (tp.OK, n * 2, n, double_number_decorator)

        arg_val = (2,)
        resp = double_number_decorator(*arg_val)
        assert isinstance(resp, tuple)
        assert isinstance(resp, TPResponse)
        assert resp.content == double_number(*arg_val)
        assert resp.status_code == tp.OK


class TestExceptions:
    exception_type_map = {
        ValueError: tp.InputError,
        RuntimeError: tp.ProcessingError,
    }

    def test_raise_exception_default(_):
        @tpify()
        def raise_exception() -> TPResponse:
            raise Exception("This could be any exception in a function")

        resp = raise_exception()
        assert resp.status_code == tp.ProcessingError
        assert isinstance(resp.content, Exception)

    def test_raise_exception_status(_):
        @tpify()
        def raise_exception():
            return (tp.InputError, ValueError("You're not allowed to do that"))

        resp = raise_exception()
        assert resp.status_code == tp.InputError
        assert isinstance(resp.content, ValueError)

    @pytest.mark.parametrize(
        "error,tp_status",
        [
            (ValueError("This is a ValueError"), tp.InputError),
            (RuntimeError, tp.ProcessingError),
            (IndentationError, tp.InputError),
        ],
    )
    def test_raise_exception_status(self, error: Exception, tp_status: tp):
        @tpify(exception_type_map=self.exception_type_map)
        def raise_exception():
            raise error

        resp = raise_exception()
        if type(resp.content) in self.exception_type_map:
            assert resp.status_code == tp_status
        else:
            assert resp.status_code == _DEFAULT_ERROR_CODE
