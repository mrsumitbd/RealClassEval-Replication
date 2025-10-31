from __future__ import annotations

import os
import shlex
import subprocess
from typing import Optional


class Shell:
    '''Wrapper around subprocess supporting dry_run mode.'''

    def __init__(self, dry_run: bool = False, safe_mode: bool = True):
        '''Initialize shell wrapper.
        Args:
            dry_run: If True, commands will be logged but not executed
            safe_mode: If True, enables additional safety checks for commands
        '''
        self.dry_run = dry_run
        self.safe_mode = safe_mode

    def _validate_command_safety(self, cmd: str) -> None:
        '''Validate command for basic safety if safe_mode is enabled.
        Args:
            cmd: Command to validate
        Raises:
            RuntimeError: If command appears unsafe
        '''
        if not self.safe_mode:
            return

        c = cmd.strip().lower()

        dangerous_substrings = [
            "rm -rf /",
            "rm -rf --no-preserve-root",
            ":(){ :|:& };:",  # fork bomb
            "mkfs",
            "mkfs.ext",
            "fdisk",
            "parted",
            "poweroff",
            "shutdown",
            "reboot",
            "halt",
            ">| /",  # clobber root files
        ]
        if any(s in c for s in dangerous_substrings):
            raise RuntimeError(f"Unsafe command blocked by safe_mode: {cmd}")

        # Block piping remote script directly into a shell
        pipe_shells = ["| sh", "| bash", "| zsh", "| ksh"]
        if ("curl" in c or "wget" in c) and any(p in c for p in pipe_shells):
            raise RuntimeError(
                f"Unsafe command (remote script pipe) blocked: {cmd}")

        # Block writing directly to block devices using dd
        if "dd " in c and (" of=/dev/sd" in c or " of=/dev/nvme" in c or " of=/dev/mmcblk" in c):
            raise RuntimeError(
                f"Unsafe command (dd to block device) blocked: {cmd}")

        # Block rm -rf on suspicious targets
        if "rm -rf" in c:
            tokens = shlex.split(cmd)
            # find index of rm and collect targets
            try:
                i = next(i for i, t in enumerate(tokens) if t == "rm")
                targets = [t for t in tokens[i + 1:] if not t.startswith("-")]
                risky_targets = {"/", "/*", "~", "~/", "."}
                if any(t in risky_targets for t in targets):
                    raise RuntimeError(f"Unsafe rm target blocked: {cmd}")
            except StopIteration:
                pass

    def run(self, *parts: str, timeout: int = 30, cwd: Optional[str] = None) -> str:
        '''Execute a shell command and return stripped output.
        Args:
            *parts: Command parts to join with spaces
            timeout: Command timeout in seconds
            cwd: Working directory for command execution
        Returns:
            Command output as string
        Raises:
            RuntimeError: If command fails or times out
        '''
        cmd = " ".join(p for p in parts if p is not None)
        if self.safe_mode:
            self._validate_command_safety(cmd)

        if self.dry_run:
            return ""

        try:
            proc = subprocess.run(
                cmd,
                shell=True,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as e:
            raise RuntimeError(
                f"Command timed out after {timeout}s: {cmd}") from e
        except Exception as e:
            raise RuntimeError(
                f"Failed to execute command: {cmd} ({e})") from e

        if proc.returncode != 0:
            raise RuntimeError(
                f"Command failed with exit code {proc.returncode}: {cmd}\n"
                f"stdout: {proc.stdout.strip()}\n"
                f"stderr: {proc.stderr.strip()}"
            )

        return proc.stdout.strip()

    def run_check(self, *parts: str, timeout: int = 30, cwd: Optional[str] = None) -> bool:
        '''Execute a command and return True if successful, False otherwise.
        Args:
            *parts: Command parts to join with spaces
            timeout: Command timeout in seconds
            cwd: Working directory for command execution
        Returns:
            True if command succeeded, False otherwise
        '''
        if self.dry_run:
            return True
        try:
            self.run(*parts, timeout=timeout, cwd=cwd)
            return True
        except Exception:
            return False

    def write_file(
        self,
        path: str,
        content: str,
        mode: str = "w",
        create_dirs: bool = True,
        permissions: Optional[int] = None,
    ) -> None:
        '''Write content to a file (respects dry_run mode).
        Args:
            path: File path to write to
            content: Content to write
            mode: File write mode (default: "w")
            create_dirs: Create parent directories if they don't exist
            permissions: Unix file permissions (e.g., 0o600 for user-only)
        Raises:
            RuntimeError: If file operation fails
        '''
        if self.safe_mode:
            abs_path = os.path.abspath(path)
            blocked_paths = {
                "/etc/shadow",
                "/etc/passwd",
                "/etc/sudoers",
            }
            if abs_path in blocked_paths:
                raise RuntimeError(
                    f"Writing to critical system file blocked by safe_mode: {abs_path}")
            if abs_path == "/" or abs_path.endswith("//"):
                raise RuntimeError("Refusing to write to root directory")

        if self.dry_run:
            return

        try:
            parent = os.path.dirname(os.path.abspath(path)) or "."
            if create_dirs:
                os.makedirs(parent, exist_ok=True)

            with open(path, mode) as f:
                f.write(content)

            if permissions is not None:
                os.chmod(path, permissions)
        except Exception as e:
            raise RuntimeError(f"Failed to write file '{path}': {e}") from e
