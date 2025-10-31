
import os
import subprocess
import logging
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
            r"rm\s+-rf",
            r"sudo",
            r"dd\s+if=",
            r"mkfs",
            r"chmod\s+777",
            r"mv\s+.*\s+-f",
            r"cp\s+.*\s+-f",
            r"ln\s+.*\s+-f",
            r"truncate\s+.*\s+-s",
        ]

        for pat in unsafe_patterns:
            if re.search(pat, cmd, re.IGNORECASE):
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
        cmd = " ".join(parts)
        self._validate_command_safety(cmd)

        if self.dry_run:
            logger.info("[dry-run] %s", cmd)
            return ""

        try:
            result = subprocess.run(
                parts,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd,
                check=True,
            )
            return result.stdout.strip()
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(
                f"Command timed out after {timeout}s: {cmd}") from exc
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(
                f"Command failed with exit {exc.returncode}: {cmd}\n"
                f"stdout: {exc.stdout}\nstderr: {exc.stderr}"
            ) from exc

    def run_check(self, *parts: str, timeout: int = 30, cwd: Optional[str] = None) -> bool:
        """Execute a command and return True if successful, False otherwise.

        Args:
            *parts: Command parts to join with spaces
            timeout: Command timeout in seconds
            cwd: Working directory for command execution

        Returns:
            True if command succeeded, False otherwise
        """
        cmd = " ".join(parts)
        self._validate_command_safety(cmd)

        if self.dry_run:
            logger.info("[dry-run] %s", cmd)
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
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            logger.error(
                "Command timed out after %s seconds: %s", timeout, cmd)
            return False

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
            logger.info("[dry-run] write_file %s", path)
            return

        try:
            p = Path(path)
            if create_dirs:
                p.parent.mkdir(parents=True, exist_ok=True)
            with p.open(mode, encoding="utf-8") as f:
                f.write(content)
            if permissions is not None:
                os.chmod(p, permissions)
        except Exception as exc:
            raise RuntimeError(
                f"Failed to write file {path!r}: {exc}") from exc
