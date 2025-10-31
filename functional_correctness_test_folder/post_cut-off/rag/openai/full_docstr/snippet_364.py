
from dataclasses import dataclass, field
from typing import Any, Optional, Dict


@dataclass
class CLIResult:
    '''Standard result structure for CLI commands.'''
    success: bool
    message: str = ""
    data: Any = None
    error: Optional[str] = None

    def is_success(self) -> bool:
        '''Check if the result represents success.'''
        return self.success

    def to_dict(self) -> Dict[str, Any]:
        '''Convert result to dictionary for JSON output.'''
        result: Dict[str, Any] = {
            "success": self.success,
            "message": self.message,
            "data": self.data,
            "error": self.error,
        }
        # Remove keys with None values for cleaner output
        return {k: v for k, v in result.items() if v is not None}
