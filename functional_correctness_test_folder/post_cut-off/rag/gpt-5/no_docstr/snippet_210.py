from __future__ import annotations

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

        try:
            tokens = shlex.split(cmd)
        except ValueError:
            tokens = cmd.split()

        if not tokens:
            return

        # Strip common wrappers
        while tokens and tokens[0] in ('sudo',):
            tokens = tokens[1:]

        if not tokens:
            return

        prog = tokens[0]

        # Dangerous power actions
        if prog in ('shutdown', 'reboot', 'halt', 'poweroff'):
            raise RuntimeError(f'Unsafe command blocked by safe_mode: {cmd}')

        # rm -rf safety checks (prevent root deletion)
        if prog == 'rm':
            opts = [t for t in tokens[1:] if t.startswith('-')]
            args = [t for t in tokens[1:] if not t.startswith('-')]

            has_r = any('r' in o for o in opts)
            has_f = any('f' in o for o in opts)
            no_preserve_root = any('--no-preserve-root' in o for o in opts)

            if (has_r and has_f) or any(o in ('-rf', '-fr') for o in opts) or no_preserve_root:
                # Block attempts to remove root or immediate wildcards under root
                forbidden_targets = {'/', '/*', '"/"', "'/'"}
                if any(a in forbidden_targets for a in args):
                    raise RuntimeError(
                        f'Unsafe command blocked by safe_mode: {cmd}')
                # Be conservative: block if explicitly targeting root directory
                if any(a.rstrip('/') == '/' for a in args):
                    raise RuntimeError(
                        f'Unsafe command blocked by safe_mode: {cmd}')

        # dd writing directly to disks (very conservative block)
        if prog == 'dd':
            of_args = [t for t in tokens if t.startswith('of=')]
            dangerous_prefixes = ('/dev/sd', '/dev/nvme',
                                  '/dev/vd', '/dev/disk')
            for ofa in of_args:
                target = ofa[3:]
                if any(target.startswith(p) for p in dangerous_prefixes):
                    raise RuntimeError(
                        f'Unsafe command blocked by safe_mode: {cmd}')

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
        if not parts:
            raise RuntimeError('No command provided')

        cmd_str = ' '.join(parts)
        self._validate_command_safety(cmd_str)

        if self.dry_run:
            logger.info('[dry-run] Would run: %s', cmd_str)
            return ''

        # Choose shell mode when a single string is passed, to allow shell features.
        shell_mode = len(parts) == 1
        if shell_mode:
            args = cmd_str  # type: ignore[assignment]
        else:
            args = list(parts)

        try:
            proc = subprocess.run(
                args,  # type: ignore[arg-type]
                shell=shell_mode,
                capture_output=True,
                text=True,
                cwd=cwd,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(
                f'Command timed out after {timeout}s: {cmd_str}') from exc
        except Exception as exc:
            raise RuntimeError(
                f'Failed to execute command: {cmd_str} ({exc})') from exc

        stdout = (proc.stdout or '').strip()
        stderr = (proc.stderr or '').strip()

        if proc.returncode != 0:
            msg = f'Command failed ({proc.returncode}): {cmd_str}'
            if stdout:
                msg += f'\nstdout: {stdout}'
            if stderr:
                msg += f'\nstderr: {stderr}'
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
            logger.info('[dry-run] Would run (check): %s', ' '.join(parts))
            return True

        try:
            self.run(*parts, timeout=timeout, cwd=cwd)
            return True
        except Exception as exc:
            logger.debug('run_check failed: %s', exc)
            return False

    def write_file(
        self,
        path: str,
        content: str,
        mode: str = 'w',
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
        if self.dry_run:
            logger.info('[dry-run] Would write file: %s (mode=%s, perms=%s)',
                        path, mode, oct(permissions) if permissions is not None else None)
            return

        try:
            directory = os.path.dirname(path)
            if directory and create_dirs:
                os.makedirs(directory, exist_ok=True)

            with open(path, mode, encoding='utf-8') as f:
                f.write(content)

            if permissions is not None:
                os.chmod(path, permissions)
        except Exception as exc:
            raise RuntimeError(f'Failed to write file {path}: {exc}') from exc
