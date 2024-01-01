from typing import Callable, Tuple

import pytest
from tpify import Response, StatusResponse, tpify
from tpify.core import analysis


class TestAnalysisFunctions:
    funcs = (
        analysis.is_informational,
        analysis.is_success,
        analysis.is_redirect,
        analysis.is_client_error,
        analysis.is_server_error,
        analysis.is_error,
    )

    @staticmethod
    @tpify
    def return_status_code(status_code):
        return StatusResponse(
            status_code=status_code, content=f"Testing status code {status_code}"
        )

    @pytest.mark.parametrize(
        "should_succeed,status_codes",
        [
            ((analysis.is_informational,), range(100, 200)),
            ((analysis.is_success,), range(200, 300)),
            ((analysis.is_redirect,), range(300, 400)),
            ((analysis.is_client_error, analysis.is_error), range(400, 500)),
            ((analysis.is_server_error, analysis.is_error), range(500, 600)),
        ],
    )
    def test_analysis_functions(
        self, should_succeed: Tuple[Callable, ...], status_codes: range
    ):
        for status_code in status_codes:
            resp: Response = TestAnalysisFunctions.return_status_code(status_code)
            assert resp.status_code == status_code
            for func in self.funcs:
                analysis_resp: Response = func(resp)
                assert analysis_resp.content == (func in should_succeed)
                assert analysis_resp.status_code == 200
