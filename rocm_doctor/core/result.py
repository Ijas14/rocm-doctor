from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from enum import Enum

class Status(Enum):
    OK = "OK"
    WARNING = "WARNING"
    ERROR = "ERROR"
    INFO = "INFO"
    NA = "N/A"

@dataclass
class CheckResult:
    name: str
    status: Status
    data: Dict[str, Any] = field(default_factory=dict)
    message: Optional[str] = None
    error: Optional[str] = None
