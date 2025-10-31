
import os
import subprocess
from pathlib import Path
from typing import Optional, List


class Shell:
    """
    A small helper for running shell commands with optional safety checks,
    dry‑run support, and file writing utilities.
    """

    # Simple list of potentially dangerous command patterns
    _DANGEROUS_PATTERNS: List[str] = [
        r"rm\s+-rf",
        r"sudo",
        r"mkfs",
        r":\s*rm\s+-rf",
        r"dd\s+if=",
        r"dd\s+of=",
    ]

    def __init__(self, dry_run: bool = False, safe_mode: bool = True):
        """
        Parameters
        ----------
        dry_run : bool, optional
            If True, commands are not actually executed; run() returns an empty string.
        safe_mode : bool, optional
            If True, commands containing dangerous patterns raise ValueError.
        """
        self.dry_run = dry_run
        self.safe_mode = safe_mode

    def _validate_command_safety(self, cmd: str) -> None:
        """
        Validate that the command does not contain dangerous patterns when safe_mode is enabled.
        """
        if not self.safe_mode:
            return

        import re

        for pattern in self._DANGEROUS_PATTERNS:
            if re.search(pattern, cmd, re.IGNORECASE):
                raise ValueError(f"Unsafe command detected: {cmd!r}")

    def run(self, *parts: str, timeout: int = 30, cwd: Optional[str] = None) -> str:
        """
        Execute a command composed of the given parts and return its stdout.

        Parameters
        ----------
        *parts : str
            The command and its arguments.
        timeout : int, optional
            Timeout in seconds.
        cwd : str, optional
            Working directory for the command.

        Returns
        -------
        str
            The command's stdout.
        """
        if not parts:
            raise ValueError("No command parts provided")

        cmd = " ".join(parts)
        self._validate_command_safety(cmd)

        if self.dry_run:
            return ""

        result = subprocess.run(
            parts,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        result.check_returncode()
        return result.stdout

    def run_check(self, *parts: str, timeout: int = 30, cwd: Optional[str] = None) -> bool:
        """
        Execute a command and return True if it exits with status 0, False otherwise.

        Parameters
        ----------
        *parts : str
            The command and its arguments.
        timeout : int, optional
            Timeout in seconds.
        cwd : str, optional
            Working directory for the command.

        Returns
        -------
        bool
            True if the command succeeded, False otherwise.
        """
        if not parts:
            raise ValueError("No command parts provided")

        cmd = " ".join(parts)
        self._validate_command_safety(cmd)

        if self.dry_run:
            return True

        try:
            subprocess.run(
                parts,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=True,
            )
            return True
        except subprocess.CalledProcessError:
            return False
        except subprocess.TimeoutExpired:
            return False

    def write_file(
        self,
        path: str,
        content: str,
        mode: str = "w",
        create_dirs: bool = True,
        permissions: Optional[int] = None,
    ) -> None:
        """
        Write content to a file, optionally creating parent directories and setting permissions.

        Parameters
        ----------
        path : str
            Target file path.
        content : str
            Text to write.
        mode : str, optional
            File mode, e.g. 'w', 'a', 'wb'.
        create_dirs : bool, optional
            Create parent directories if they do not exist.
        permissions : int, optional
            File mode to set (e.g., 0o644). Ignored if None.
        """
        file_path = Path(path)

        if create_dirs:
            file_path.parent.mkdir(parents=True, exist_ok=True)

        with file_path.open(mode, encoding="utf-8" if "b" not in mode else None) as f:
            f.write(content)

        if permissions is not None:
            os.chmod(file_path, permissions)
