from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple


@dataclass
class StatusResponse:
    status_code: int = 100
    content: Optional[Any] = None


@dataclass
class Response:
    func: Optional[Callable] = None
    args: Optional[Tuple] = None
    kwargs: Optional[Dict[str, Any]] = None
    status_code: int = 100
    content: Optional[Any] = None
    headers: Dict[str, Any] = field(default_factory=dict)
    elapsed: float = 0.0
    history: List["Response"] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"<Response [{self.status_code}]>"
