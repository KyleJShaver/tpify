from abc import ABC
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple


@dataclass
class _ResponseBase(ABC):
    status_code: int = 100
    content: Optional[Any] = None

    def __repr__(self) -> str:
        raise NotImplementedError


@dataclass
class StatusResponse(_ResponseBase):
    def __repr__(self) -> str:
        return f"<StatusResponse [{self.status_code}]>"


@dataclass
class Response(_ResponseBase):
    func: Optional[Callable] = None
    args: Optional[Tuple] = None
    kwargs: Optional[Dict[str, Any]] = None
    headers: Dict[str, Any] = field(default_factory=dict)
    elapsed: float = 0.0
    history: List["Response"] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"<Response [{self.status_code}]>"
