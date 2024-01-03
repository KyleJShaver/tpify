from enum import IntEnum
from typing import Iterable


class TPStatus(IntEnum):
    Unknown = 1
    OK = 2
    Continue = 3
    InputError = 4
    ProcessingError = 5


class TPStatusCustom(IntEnum):
    pass


def append_statuses(statuses: Iterable[str]) -> TPStatusCustom:
    return TPStatusCustom(
        "TPStatusCustom", [status.name for status in TPStatus] + list(statuses)
    )
