
import logging
import os
import subprocess
from pathlib import Path
from typing import Optional

log = logging.getLogger(__name__)


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
        dangerous_patterns = [
            r"\brm\b",
            r"\bsudo\b",
            r"\bmv\b",
            r"\bdd\b",
            r"\bmkfs\b",
            r"\bchmod\b",
            r"\bchown\b",
        ]

        for pat in dangerous_patterns:
            if pat in cmd:
                # For rm, check for -rf or -r or -f
                if "rm" in cmd:
                    if "-rf" in cmd or "-r" in cmd or "-f" in cmd:
                        raise RuntimeError(f"Unsafe command detected: {cmd!r}")
                else:
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
            log.info("[dry-run] %s", cmd)
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
            raise RuntimeError(f"Command timed out: {cmd}") from exc
        except Exception as exc:
            raise RuntimeError(f"Command failed to start: {cmd}") from exc

        if result.returncode != 0:
            raise RuntimeError(
                f"Command failed (exit {result.returncode}): {cmd}\n"
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
        cmd = " ".join(parts)
        self._validate_command_safety(cmd)

        if self.dry_run:
            log.info("[dry-run] %s", cmd)
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
        except Exception:
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
            log.info("[dry-run] write_file %s", path)
            return

        p = Path(path)
        if create_dirs:
            try:
                p.parent.mkdir(parents=True, exist_ok=True)
            except Exception as exc:
                raise RuntimeError(
                    f"Failed to create directories for {path}") from exc

        try:
            with p.open(mode, encoding="utf-8") as f:
                f.write(content)
        except Exception as exc:
            raise RuntimeError(f"Failed to write file {path}") from exc

        if permissions is not None:
            try:
                os.chmod(p, permissions)
            except Exception as exc:
                raise RuntimeError(
                    f"Failed to set permissions on {path}") from exc
