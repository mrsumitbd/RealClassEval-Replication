import logging
import os
import re
import subprocess
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
        if not self.safe_mode:
            return

        lc = cmd.lower().strip()

        if not lc:
            raise RuntimeError('Empty command is not allowed')

        if ':(){ :|:& };:' in lc:
            raise RuntimeError('Unsafe command detected (fork bomb pattern)')

        if 'rm' in lc and '-rf' in lc:
            if re.search(r'\s/(?:\s|$)', lc) or '/*' in lc or '--no-preserve-root' in lc:
                raise RuntimeError('Unsafe rm -rf against root detected')

        if re.search(r'\bdd\b', lc) and re.search(r'\bof=/dev/(sd|nvme|vd|mmcblk)', lc):
            raise RuntimeError('Unsafe dd to block device detected')

        if re.search(r'\bmkfs(\.|)\b', lc) and re.search(r'/dev/(sd|nvme|vd|mmcblk)', lc):
            raise RuntimeError(
                'Unsafe filesystem operation on block device detected')

        if re.search(r'>\s*/dev/(sd|nvme|vd|mmcblk)', lc):
            raise RuntimeError('Unsafe redirection to block device detected')

        if re.search(r'\b(chmod|chown)\b.*\b(-r|-R)\b.*\s/(?:\s|$)', lc):
            raise RuntimeError(
                'Recursive permission/ownership change on root detected')

        if re.search(r'\bkill\s+-9\s+1\b', lc):
            raise RuntimeError('Attempt to kill PID 1 detected')

        if re.search(r'\b(init\s+0|poweroff|halt|reboot|shutdown(\s+-\w+)*|systemctl\s+(poweroff|reboot|halt))\b', lc):
            raise RuntimeError('System power operation detected')

        if re.search(r'\|\s*(sh|bash|zsh|dash)\b', lc):
            raise RuntimeError(
                'Piping into a shell is not allowed in safe_mode')

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
        cmd = ' '.join(p for p in parts if p is not None).strip()
        self._validate_command_safety(cmd)

        if self.dry_run:
            logger.info('[dry-run] shell: %s', cmd)
            return ''

        logger.debug('Executing shell command: %s', cmd)
        try:
            proc = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd,
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError(
                f'Command timed out after {timeout}s: {cmd}') from None
        except Exception as exc:
            raise RuntimeError(
                f'Failed to execute command: {cmd} ({exc})') from exc

        stdout = (proc.stdout or '').strip()
        stderr = (proc.stderr or '').strip()

        if proc.returncode != 0:
            msg = f'Command failed (exit {proc.returncode}): {cmd}'
            if stdout:
                msg += f'\nstdout:\n{stdout}'
            if stderr:
                msg += f'\nstderr:\n{stderr}'
            raise RuntimeError(msg)

        return stdout

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
            cmd = ' '.join(p for p in parts if p is not None).strip()
            try:
                self._validate_command_safety(cmd)
            except RuntimeError as exc:
                logger.warning(
                    '[dry-run] unsafe command rejected: %s (%s)', cmd, exc)
                return False
            logger.info('[dry-run] shell (check): %s', cmd)
            return True

        try:
            self.run(*parts, timeout=timeout, cwd=cwd)
            return True
        except Exception as exc:
            logger.warning('Command failed: %s', exc)
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
        if not path:
            raise RuntimeError('File path must not be empty')

        dirpath = os.path.dirname(os.path.abspath(path))
        if self.dry_run:
            logger.info('[dry-run] write file: %s (mode=%s, perms=%s)', path,
                        mode, oct(permissions) if permissions is not None else None)
            return

        try:
            if create_dirs and dirpath and not os.path.exists(dirpath):
                os.makedirs(dirpath, exist_ok=True)

            if 'b' in mode:
                with open(path, mode) as f:
                    if isinstance(content, str):
                        data = content.encode('utf-8')
                    else:
                        data = content  # type: ignore
                    f.write(data)  # type: ignore
            else:
                with open(path, mode, encoding='utf-8') as f:
                    f.write(content)

            if permissions is not None:
                os.chmod(path, permissions)
        except OSError as exc:
            raise RuntimeError(f'Failed to write file {path}: {exc}') from exc
