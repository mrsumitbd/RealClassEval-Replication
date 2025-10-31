
from dataclasses import dataclass, asdict, field
from typing import Any, Optional


@dataclass
class CLIResult:
    '''Standard result structure for CLI commands.'''
    success: bool = field(default=False)
    message: Optional[str] = field(default=None)
    data: Optional[Any] = field(default=None)

    def is_success(self) -> bool:
        return self.success

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
