
from dataclasses import dataclass
from typing import Any


@dataclass
class CLIResult:
    '''Standard result structure for CLI commands.'''
    success: bool
    message: str
    data: Any = None

    def is_success(self) -> bool:
        '''Check if the result represents success.'''
        return self.success

    def to_dict(self) -> dict[str, Any]:
        '''Convert result to dictionary for JSON output.'''
        result_dict = {
            'success': self.success,
            'message': self.message
        }
        if self.data is not None:
            result_dict['data'] = self.data
        return result_dict
