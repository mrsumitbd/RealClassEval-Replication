
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class CLIResult:
    """Standard result structure for CLI commands."""

    success: bool = field(default=False)
    message: str = field(default_factory=str)
    data: Any = field(default=None)

    def is_success(self) -> bool:
        """Return True if the command succeeded."""
        return self.success

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the result."""
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data,
        }
