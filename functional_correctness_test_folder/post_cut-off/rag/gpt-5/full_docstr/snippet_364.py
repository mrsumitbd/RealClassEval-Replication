from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class CLIResult:
    """Standard result structure for CLI commands."""
    exit_code: int = 0
    message: Optional[str] = None
    data: Any = None
    error: Optional[str] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    meta: Optional[dict[str, Any]] = None

    def is_success(self) -> bool:
        """Check if the result represents success."""
        return self.exit_code == 0 and (self.error is None or self.error == "")

    def to_dict(self) -> dict[str, Any]:
        """Convert result to dictionary for JSON output."""
        payload: dict[str, Any] = {
            "success": self.is_success(),
            "exit_code": self.exit_code,
            "message": self.message,
            "data": self.data,
            "error": self.error,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "meta": self.meta,
        }
        return {k: v for k, v in payload.items() if v is not None}
