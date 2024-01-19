import pytest

from tpify import TPResult, err, ok, tpify_result


def double_number(n: int) -> int:
    return n * 2


def append_number(l: list, n: int) -> list:
    l.append(n)
    return l


@pytest.mark.parametrize("n", [2])
def test_double_number_result_ok(n):
    @tpify_result
    def double_number_decorator_tp(n: int):
        return double_number(n)

    result = double_number_decorator_tp(n)
    assert isinstance(result, TPResult)
    assert result.is_ok()
    assert not result.is_err()
    assert result.ok == 4
    assert result.err == None


@pytest.mark.parametrize("l,n", [([0, 1], 2)])
def test_append_number_result_ok(l, n):
    @tpify_result
    def append_number_decorator_tp(l: list, n: int):
        return append_number(l, n)

    result = append_number_decorator_tp(l, n)
    assert isinstance(result, TPResult)
    assert result.is_ok()
    assert not result.is_err()
    assert result.ok == l
    assert result.ok is l
    assert result.err == None


@pytest.mark.parametrize("n", [{"set"}])
def test_double_number_result_err(n):
    @tpify_result
    def double_number_decorator_tp(n: int):
        return double_number(n)

    result = double_number_decorator_tp(n)
    assert isinstance(result, TPResult)
    assert not result.is_ok()
    assert result.is_err()
    assert result.ok == None
    assert result.err is not None
    assert isinstance(result.err, TypeError)


def test_invalid_initialization():
    result = TPResult("Something", "Also Something")
    assert result.is_err()
    assert isinstance(result.err, ValueError)


def test_repr():
    result = err("Some Error")
    assert str(result) == "<TPResult [err]>"
    result = TPResult("Something", "Also Something")
    assert str(result) == "<TPResult [err]>"
    result = ok("Some Value")
    assert str(result) == "<TPResult [ok]>"
