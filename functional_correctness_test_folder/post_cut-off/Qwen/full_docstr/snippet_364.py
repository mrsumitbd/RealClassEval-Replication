
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class CLIResult:
    '''Standard result structure for CLI commands.'''
    success: bool
    message: str = ""
    data: Optional[Any] = None

    def is_success(self) -> bool:
        '''Check if the result represents success.'''
        return self.success

    def to_dict(self) -> dict[str, Any]:
        '''Convert result to dictionary for JSON output.'''
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data
        }
