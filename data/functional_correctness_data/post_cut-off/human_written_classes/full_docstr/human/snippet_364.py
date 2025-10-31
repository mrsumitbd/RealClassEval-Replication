from dataclasses import dataclass
from typing import Any, TypeVar

@dataclass
class CLIResult:
    """Standard result structure for CLI commands."""
    status: str
    message: str
    data: dict[str, Any] | None = None
    exit_code: int = 0

    def is_success(self) -> bool:
        """Check if the result represents success."""
        return self.status in ['success', 'skipped', 'dry_run']

    def to_dict(self) -> dict[str, Any]:
        """Convert result to dictionary for JSON output."""
        result = {'status': self.status, 'message': self.message}
        if self.data:
            result.update(self.data)
        return result