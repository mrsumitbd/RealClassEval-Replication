
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class CLIResult:
    def is_success(self) -> bool:
        return False

    def to_dict(self) -> Dict[str, Any]:
        return {}
