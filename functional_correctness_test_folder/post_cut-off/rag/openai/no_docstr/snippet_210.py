
import logging
import os
import subprocess
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class Shell:
    """Wrapper around subprocess supporting dry_run mode."""

    def __init__(self, dry_run: bool = False, safe_mode: bool = True):
        """Initialize shell wrapper.

        Args:
            dry_run: If True, commands will be logged but not executed
            safe_mode: If True, enables additional safety checks for commands
        """
        self.dry_run = dry_run
        self.safe_mode = safe_mode

    def _validate_command_safety(self, cmd: str) -> None:
        """Validate command for basic safety if safe_mode is enabled.

        Args:
            cmd: Command to validate

        Raises:
            RuntimeError: If command appears unsafe
        """
        if not self.safe_mode:
            return

        # Very simple safety checks – expand as needed
        unsafe_patterns = [
            r"\brm\b",
            r"\brm\s+-rf\b",
            r"\bsudo\b",
            r"\bdd\b",
            r"\bmkfs\b",
            r"\bshutdown\b",
            r"\breboot\b",
            r"\b:(){\s*;\s*};\b",  # fork bomb
        ]
        lower = cmd.lower()
        for pat in unsafe_patterns:
            if pat in lower:
                raise RuntimeError(f"Unsafe command detected: {cmd!r}")

    def run(self, *parts: str, timeout: int = 30, cwd: Optional[str] = None) -> str:
        """Execute a shell command and return stripped output.

        Args:
            *parts: Command parts to join with spaces
            timeout: Command timeout in seconds
            cwd: Working directory for command execution

        Returns:
            Command output as string

        Raises:
            RuntimeError: If command fails or times out
        """
        cmd_str = " ".join(parts)
        self._validate_command_safety(cmd_str)

        if self.dry_run:
            logger.info("[dry-run] %s", cmd_str)
            return ""

        try:
            result = subprocess.run(
                parts,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(
                f"Command timed out after {timeout}s: {cmd_str}") from exc
        except OSError as exc:
            raise RuntimeError(
                f"Failed to execute command: {cmd_str}") from exc

        if result.returncode != 0:
            raise RuntimeError(
                f"Command failed (exit {result.returncode}): {cmd_str}\n"
                f"stdout: {result.stdout}\nstderr: {result.stderr}"
            )

        return result.stdout.strip()

    def run_check(self, *parts: str, timeout: int = 30, cwd: Optional[str] = None) -> bool:
        """Execute a command and return True if successful, False otherwise.

        Args:
            *parts: Command parts to join with spaces
            timeout: Command timeout in seconds
            cwd: Working directory for command execution

        Returns:
            True if command succeeded, False otherwise
        """
        cmd_str = " ".join(parts)
        self._validate_command_safety(cmd_str)

        if self.dry_run:
            logger.info("[dry-run] %s", cmd_str)
            return True

        try:
            result = subprocess.run(
                parts,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd,
                check=False,
            )
        except (subprocess.TimeoutExpired, OSError):
            return False

        return result.returncode == 0

    def write_file(
        self,
        path: str,
        content: str,
        mode: str = "w",
        create_dirs: bool = True,
        permissions: Optional[int] = None,
    ) -> None:
        """Write content to a file (respects dry_run mode).

        Args:
            path: File path to write to
            content: Content to write
            mode: File write mode (default: "w")
            create_dirs: Create parent directories if they don't exist
            permissions: Unix file permissions (e.g., 0o600 for user-only)

        Raises:
            RuntimeError: If file operation fails
        """
        if self.dry_run:
            logger.info("[dry-run] write_file %s (mode=%s, perms=%s)",
                        path, mode, permissions)
            return

        try:
            if create_dirs:
                parent = Path(path).parent
                parent.mkdir(parents=True, exist_ok=True)

            with open(path, mode, encoding="utf-8") as fp:
                fp.write(content)

            if permissions is not None:
                os.chmod(path, permissions)
        except OSError as exc:
            raise RuntimeError(f"Failed to write file {path!r}") from exc
