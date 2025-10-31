import os
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
        # Basic checks: prevent obvious destructive commands
        dangerous = [
            'rm -rf /', 'rm -rf /*', 'rm -rf --no-preserve-root /',
            'mkfs', 'dd if=', '>:'
        ]
        for d in dangerous:
            if d in cmd:
                raise RuntimeError(
                    f"Unsafe command detected: '{d}' in '{cmd}'")
        # Prevent empty command
        if not cmd.strip():
            raise RuntimeError("Empty command is not allowed in safe_mode")

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
        cmd = " ".join(parts)
        self._validate_command_safety(cmd)
        if self.dry_run:
            print(f"[dry_run] Would run: {cmd}")
            return ""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout,
                cwd=cwd,
                universal_newlines=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Command failed: {cmd}\n{e.stderr.strip()}") from e
        except subprocess.TimeoutExpired as e:
            raise RuntimeError(
                f"Command timed out after {timeout}s: {cmd}") from e

    def run_check(self, *parts: str, timeout: int = 30, cwd: Optional[str] = None) -> bool:
        '''Execute a command and return True if successful, False otherwise.
        Args:
            *parts: Command parts to join with spaces
            timeout: Command timeout in seconds
            cwd: Working directory for command execution
        Returns:
            True if command succeeded, False otherwise
        '''
        cmd = " ".join(parts)
        self._validate_command_safety(cmd)
        if self.dry_run:
            print(f"[dry_run] Would run: {cmd}")
            return True
        try:
            subprocess.run(
                cmd,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout,
                cwd=cwd,
                universal_newlines=True
            )
            return True
        except Exception:
            return False

    def write_file(self, path: str, content: str, mode: str = 'w', create_dirs: bool = True, permissions: Optional[int] = None) -> None:
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
        if self.dry_run:
            print(
                f"[dry_run] Would write to {path} (mode={mode}, permissions={permissions}):\n{content}")
            return
        try:
            dirpath = os.path.dirname(path)
            if create_dirs and dirpath and not os.path.exists(dirpath):
                os.makedirs(dirpath, exist_ok=True)
            with open(path, mode) as f:
                f.write(content)
            if permissions is not None:
                os.chmod(path, permissions)
        except Exception as e:
            raise RuntimeError(f"Failed to write file '{path}': {e}") from e
