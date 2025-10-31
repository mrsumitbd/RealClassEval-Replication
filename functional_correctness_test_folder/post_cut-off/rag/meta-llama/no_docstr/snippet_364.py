
from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class CLIResult:
    """Standard result structure for CLI commands."""
    status: str
    message: str

    def is_success(self) -> bool:
        """Check if the result represents success."""
        return self.status == 'success'

    def to_dict(self) -> dict[str, Any]:
        """Convert result to dictionary for JSON output."""
        return asdict(self)
