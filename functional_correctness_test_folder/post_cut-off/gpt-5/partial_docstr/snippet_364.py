from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class CLIResult:
    '''Standard result structure for CLI commands.'''
    exit_code: int = 0
    stdout: str = ""
    stderr: str = ""
    message: Optional[str] = None
    data: Optional[Any] = None
    meta: dict[str, Any] = field(default_factory=dict)

    def is_success(self) -> bool:
        return self.exit_code == 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.is_success(),
            "exit_code": self.exit_code,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "message": self.message,
            "data": self.data,
            "meta": self.meta.copy(),
        }
