
from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class CLIResult:
    return_code: int
    stdout: str
    stderr: str

    def is_success(self) -> bool:
        return self.return_code == 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
