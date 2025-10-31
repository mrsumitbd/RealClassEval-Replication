
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class CLIResult:
    """Standard result structure for CLI commands."""
    success: bool
    message: str
    data: Dict[str, Any]

    def is_success(self) -> bool:
        """Check if the result represents success."""
        return self.success

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary for JSON output."""
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data
        }
