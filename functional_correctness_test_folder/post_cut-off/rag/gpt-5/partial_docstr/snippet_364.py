from dataclasses import dataclass
from typing import Any, Optional, Dict


@dataclass
class CLIResult:
    """Standard result structure for CLI commands."""
    success: bool = True
    message: Optional[str] = None
    data: Any = None

    def is_success(self) -> bool:
        """Check if the result represents success."""
        return self.success

    def to_dict(self) -> dict[str, Any]:
        """Convert result to dictionary for JSON output."""
        result: Dict[str, Any] = {"success": self.success}
        if self.message is not None:
            result["message"] = self.message
        if self.data is not None:
            result["data"] = self.data
        return result
