from dataclasses import dataclass, field
from typing import Any, Optional, Dict


@dataclass
class CLIResult:
    """Standard result structure for CLI commands."""
    success: bool
    message: Optional[str] = None
    data: Optional[Any] = None
    error: Optional[str] = None

    def is_success(self) -> bool:
        """Check if the result represents success."""
        return self.success

    def to_dict(self) -> dict[str, Any]:
        """Convert result to dictionary for JSON output."""
        result: Dict[str, Any] = {
            "success": self.success
        }
        if self.message is not None:
            result["message"] = self.message
        if self.data is not None:
            result["data"] = self.data
        if self.error is not None:
            result["error"] = self.error
        return result
