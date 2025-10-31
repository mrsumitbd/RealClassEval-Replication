
from dataclasses import dataclass, field
from typing import Any, Optional, Dict


@dataclass
class CLIResult:
    """Standard result structure for CLI commands."""

    success: bool = field(default=False)
    message: str = field(default_factory=str)
    data: Any = field(default=None)
    error: Optional[str] = field(default=None)

    def is_success(self) -> bool:
        """Check if the result represents success."""
        return self.success

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary for JSON output."""
        result: Dict[str, Any] = {
            "success": self.success,
            "message": self.message,
            "data": self.data,
        }
        if self.error is not None:
            result["error"] = self.error
        return result
