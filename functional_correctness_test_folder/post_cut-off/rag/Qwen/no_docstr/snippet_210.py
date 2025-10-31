
import os
import subprocess
import logging
from typing import Optional

logger = logging.getLogger(__name__)


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
            if 'rm -rf' in cmd:
                raise RuntimeError(
                    "Command contains unsafe operation 'rm -rf'")
            # Add more safety checks as needed

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
        if self.safe_mode:
            self._validate_command_safety(cmd)
        if self.dry_run:
            logger.info(f"Dry run: {cmd}")
            return ""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                check=True,
                timeout=timeout,
                cwd=cwd,
                capture_output=True,
                text=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {cmd}\nError: {e.stderr}")
            raise RuntimeError(f"Command failed: {cmd}") from e
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out: {cmd}")
            raise RuntimeError(f"Command timed out: {cmd}")

    def run_check(self, *parts: str, timeout: int = 30, cwd: Optional[str] = None) -> bool:
        '''Execute a command and return True if successful, False otherwise.
        Args:
            *parts: Command parts to join with spaces
            timeout: Command timeout in seconds
            cwd: Working directory for command execution
        Returns:
            True if command succeeded, False otherwise
        '''
        cmd = ' '.join(parts)
        if self.safe_mode:
            self._validate_command_safety(cmd)
        if self.dry_run:
            logger.info(f"Dry run: {cmd}")
            return True
        try:
            subprocess.run(
                cmd,
                shell=True,
                check=True,
                timeout=timeout,
                cwd=cwd
            )
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
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
        if create_dirs:
            os.makedirs(os.path.dirname(path), exist_ok=True)
        if self.dry_run:
            logger.info(f"Dry run: Write to {path} with content:\n{content}")
            return
        try:
            with open(path, mode) as f:
                f.write(content)
            if permissions is not None:
                os.chmod(path, permissions)
        except Exception as e:
            logger.error(f"Failed to write to {path}: {e}")
            raise RuntimeError(f"Failed to write to {path}") from e
