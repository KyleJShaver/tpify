from enum import IntEnum


class TPStatus(IntEnum):
    Unknown = 1
    OK = 2
    Continue = 3
    InputError = 4
    ProcessingError = 5
