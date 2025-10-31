from dataclasses import dataclass, asdict
from typing import Any, Optional, Sequence


@dataclass(slots=True)
class CLIResult:
    exit_code: int = 0
    stdout: str = ""
    stderr: str = ""
    command: Optional[Sequence[str]] = None
    duration: Optional[float] = None

    def is_success(self) -> bool:
        return self.exit_code == 0

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["success"] = self.is_success()
        return data
