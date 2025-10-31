
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class CLIResult:
    """
    Represents the result of executing a command line interface (CLI) command.

    Attributes
    ----------
    exit_code : int
        The exit status returned by the command. A value of 0 indicates success.
    stdout : str
        The standard output produced by the command.
    stderr : str
        The standard error output produced by the command.
    """
    exit_code: int
    stdout: str = field(default_factory=str)
    stderr: str = field(default_factory=str)

    def is_success(self) -> bool:
        """Return True if the command exited with status 0."""
        return self.exit_code == 0

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the CLIResult."""
        return {
            "exit_code": self.exit_code,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "success": self.is_success(),
        }
