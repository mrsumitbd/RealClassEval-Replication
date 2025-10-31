
import subprocess
import os
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
        if self.safe_mode:
            if cmd.startswith("rm -rf /") or cmd.startswith("rm -rf / ") or cmd == "rm -rf /":
                raise RuntimeError(
                    "Command appears to be attempting to delete the root directory")
            if "&&" in cmd or "||" in cmd or ";" in cmd:
                raise RuntimeError(
                    "Command contains potentially unsafe operators (&&, ||, ;)")

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
        cmd = ' '.join(parts)
        self._validate_command_safety(cmd)
        if self.dry_run:
            print(f"DRY RUN: {cmd}")
            return ""

        try:
            result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, timeout=timeout, cwd=cwd)
            return result.stdout.decode('utf-8').strip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Command failed with return code {e.returncode}: {e.output.decode('utf-8').strip()}")
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"Command timed out after {timeout} seconds")

    def run_check(self, *parts: str, timeout: int = 30, cwd: Optional[str] = None) -> bool:
        try:
            self.run(*parts, timeout=timeout, cwd=cwd)
            return True
        except RuntimeError:
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
            print(f"DRY RUN: Writing to {path}")
            return

        dir_path = os.path.dirname(path)
        if create_dirs and dir_path:
            try:
                os.makedirs(dir_path, exist_ok=True)
            except OSError as e:
                raise RuntimeError(
                    f"Failed to create directory {dir_path}: {e}")

        try:
            with open(path, mode) as f:
                f.write(content)
        except OSError as e:
            raise RuntimeError(f"Failed to write to {path}: {e}")

        if permissions is not None:
            try:
                os.chmod(path, permissions)
            except OSError as e:
                raise RuntimeError(f"Failed to set permissions on {path}: {e}")
