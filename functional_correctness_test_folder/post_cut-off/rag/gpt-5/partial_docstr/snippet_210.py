import logging
import os
import shlex
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

        # Basic fork-bomb detection
        if ':(){' in cmd and '|:&' in cmd:
            raise RuntimeError('Unsafe command detected (possible fork bomb)')

        try:
            tokens = shlex.split(cmd)
        except ValueError:
            # If command cannot be parsed, err on the side of caution
            raise RuntimeError('Unsafe or malformed command')

        if not tokens:
            return

        # Skip wrappers to get primary command
        idx = 0
        wrappers = {'sudo', 'env', 'nice', 'nohup', 'chroot'}
        while idx < len(tokens) and tokens[idx] in wrappers:
            idx += 1
        if idx >= len(tokens):
            return

        primary = tokens[idx]
        args = tokens[idx + 1:]

        destructive_always = {'mkfs', 'fdisk', 'parted', 'diskpart', 'format'}
        if primary in destructive_always:
            raise RuntimeError(f'Unsafe command detected: {primary}')

        if primary in {'shutdown', 'reboot', 'halt', 'poweroff'}:
            raise RuntimeError(f'Unsafe system control command: {primary}')

        # dd can be dangerous when writing to block devices
        if primary == 'dd':
            joined = ' '.join(args)
            if 'of=/dev/' in joined or 'of=\\dev\\' in joined:
                raise RuntimeError('Unsafe dd output target detected')

        if primary == 'rm':
            has_recursive_force = any(
                a in ('-rf', '-fr') or (a.startswith('-')
                                        and 'r' in a and 'f' in a)
                for a in args
            )
            if has_recursive_force:
                # rm -rf / or with --no-preserve-root
                if '/' in args or '--no-preserve-root' in args:
                    raise RuntimeError(
                        'Unsafe rm detected: potential root deletion')
                # rm -rf *
                if '*' in args:
                    raise RuntimeError(
                        'Unsafe rm detected: wildcard recursive delete')

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
        cmd_str = ' '.join(p for p in parts if p is not None)
        self._validate_command_safety(cmd_str)

        logger.debug('Executing command: %s (cwd=%s, timeout=%s)',
                     cmd_str, cwd, timeout)

        if self.dry_run:
            logger.info('[dry-run] Would execute: %s', cmd_str)
            return ''

        try:
            if len(parts) == 1:
                cmd_list = shlex.split(parts[0])
            else:
                cmd_list = [p for p in parts if p]

            result = subprocess.run(
                cmd_list,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=cwd,
                timeout=timeout,
                text=True,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            logger.error('Command timed out: %s', cmd_str)
            raise RuntimeError(
                f'Command timed out after {timeout}s: {cmd_str}') from exc
        except FileNotFoundError as exc:
            logger.error('Command not found: %s', cmd_str)
            raise RuntimeError(f'Command not found: {cmd_str}') from exc
        except OSError as exc:
            logger.error('OS error during command execution: %s', cmd_str)
            raise RuntimeError(
                f'OS error during command execution: {cmd_str}: {exc}') from exc

        stdout = result.stdout.strip() if result.stdout is not None else ''
        stderr = result.stderr.strip() if result.stderr is not None else ''

        if result.returncode != 0:
            logger.error('Command failed (%s): %s',
                         result.returncode, stderr or stdout)
            raise RuntimeError(
                f'Command failed with exit code {result.returncode}: {cmd_str}\n{stderr or stdout}'
            )

        logger.debug('Command succeeded: %s', stdout)
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
            cmd_str = ' '.join(p for p in parts if p is not None)
            try:
                self._validate_command_safety(cmd_str)
                logger.info('[dry-run] Would execute: %s', cmd_str)
                return True
            except RuntimeError as exc:
                logger.warning(
                    '[dry-run] Command considered unsafe: %s (%s)', cmd_str, exc)
                return False

        try:
            _ = self.run(*parts, timeout=timeout, cwd=cwd)
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
        try:
            dirpath = os.path.dirname(os.path.abspath(path))
            if create_dirs and dirpath and not os.path.isdir(dirpath):
                if self.dry_run:
                    logger.info(
                        '[dry-run] Would create directory: %s', dirpath)
                else:
                    os.makedirs(dirpath, exist_ok=True)

            if self.dry_run:
                logger.info(
                    '[dry-run] Would write file: %s (%d bytes)', path, len(content))
                if permissions is not None:
                    logger.info(
                        '[dry-run] Would set permissions %o on %s', permissions, path)
                return

            open_kwargs = {}
            if 'b' not in mode:
                open_kwargs['encoding'] = 'utf-8'

            with open(path, mode, **open_kwargs) as f:
                f.write(content)

            if permissions is not None:
                os.chmod(path, permissions)

            logger.debug('Wrote file: %s', path)
        except OSError as exc:
            raise RuntimeError(f'Failed to write file {path}: {exc}') from exc
