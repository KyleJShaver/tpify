from typing import Tuple

from httpize.core.response import Response, StatusResponse
from httpize.core.wrapper import tpify

ResponseTypes = Tuple[Response, StatusResponse]


@tpify
def _is_in_range(resp: ResponseTypes, range_val: range):
    return resp.status_code in range_val


@tpify
def is_informational(resp: ResponseTypes):
    return _is_in_range(resp, range(100, 200))


@tpify
def is_success(resp: ResponseTypes):
    return _is_in_range(resp, range(200, 300))


@tpify
def is_redirect(resp: ResponseTypes):
    return _is_in_range(resp, range(300, 400))


@tpify
def is_client_error(resp: ResponseTypes):
    return _is_in_range(resp, range(400, 500))


@tpify
def is_server_error(resp: ResponseTypes):
    return _is_in_range(resp, range(500, 600))


@tpify
def is_error(resp: ResponseTypes):
    return _is_in_range(resp, range(400, 600))
