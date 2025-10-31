
from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class CLIResult:
    '''Standard result structure for CLI commands.'''
    success: bool
    data: Any = None
    error: str = None

    def is_success(self) -> bool:
        return self.success

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
