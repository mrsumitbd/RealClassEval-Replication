
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class CLIResult:
    returncode: int
    stdout: Optional[str] = None
    stderr: Optional[str] = None

    def is_success(self) -> bool:
        return self.returncode == 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "returncode": self.returncode,
            "stdout": self.stdout,
            "stderr": self.stderr
        }
