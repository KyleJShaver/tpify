from typing import Iterable

import pytest
from tpify import TPResponse, tp, tpify, tpify_function
from tpify.core.status_code import TPStatusCustom, append_statuses
from tpify.core.wrapper import _DEFAULT_ERROR_CODE


class TestStatusCodes:
    @pytest.mark.parametrize(
        "new_codes, ",
        [("NewStatus",)],
    )
    def test_append_statuses(_, new_codes: Iterable):
        new_statuses = append_statuses(new_codes)
        assert len(new_statuses) == len(new_codes) + len(tp)
        for new_code in new_codes:
            assert isinstance(
                getattr(new_statuses, new_code),
                (
                    tp,
                    TPStatusCustom,
                ),
            )
