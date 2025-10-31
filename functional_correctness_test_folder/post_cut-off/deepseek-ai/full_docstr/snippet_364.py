
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class CLIResult:
    '''Standard result structure for CLI commands.'''

    def is_success(self) -> bool:
        '''Check if the result represents success.'''
        return False

    def to_dict(self) -> Dict[str, Any]:
        '''Convert result to dictionary for JSON output.'''
        return {}
