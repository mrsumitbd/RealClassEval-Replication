
from dataclasses import dataclass, asdict
from typing import Any, Dict


@dataclass
class CLIResult:
    '''Standard result structure for CLI commands.'''

    def is_success(self) -> bool:
        return not bool(vars(self).get('error', None))

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
