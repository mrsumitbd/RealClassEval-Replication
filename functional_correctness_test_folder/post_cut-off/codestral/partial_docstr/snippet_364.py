
from dataclasses import dataclass
from typing import Any


@dataclass
class CLIResult:
    '''Standard result structure for CLI commands.'''
    success: bool
    message: str
    data: Any = None

    def is_success(self) -> bool:
        return self.success

    def to_dict(self) -> dict[str, Any]:
        return {
            'success': self.success,
            'message': self.message,
            'data': self.data
        }
