
from dataclasses import dataclass
from typing import Any


@dataclass
class CLIResult:
    success: bool
    output: str
    error: str

    def is_success(self) -> bool:
        return self.success

    def to_dict(self) -> dict[str, Any]:
        return {
            'success': self.success,
            'output': self.output,
            'error': self.error
        }
