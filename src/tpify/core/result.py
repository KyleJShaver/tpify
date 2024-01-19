from typing import Any, Optional


class TPResult:
    __slots__ = ("ok", "err")

    def __init__(self, ok: Optional[Any] = None, err: Optional[Any] = None):
        if ok is not None and err is not None:
            self.ok = None
            self.err = ValueError("`ok` and `err` can not both have a value")
            return None
        self.ok = ok
        self.err = err

    def __repr__(self) -> str:
        return f"<TPResult [{'err' if self.is_err() else 'ok'}]>"

    def is_err(self):
        return self.err is not None

    def is_ok(self):
        return not self.is_err()


def ok(value: Optional[Any]) -> TPResult:
    return TPResult(ok=value)


def err(value: Optional[Any]) -> TPResult:
    return TPResult(err=value)
