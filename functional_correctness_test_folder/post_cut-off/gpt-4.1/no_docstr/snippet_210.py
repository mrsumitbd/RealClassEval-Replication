
import os
import subprocess
from typing import Optional


class Shell:

    def __init__(self, dry_run: bool = False, safe_mode: bool = True):
        self.dry_run = dry_run
        self.safe_mode = safe_mode
        self._dangerous_patterns = [
            'rm -rf /', 'rm -rf --no-preserve-root /', 'mkfs', 'dd if=', '>:',
            'shutdown', 'reboot', 'halt', 'init 0', 'init 6', ':(){ :|:& };:', 'forkbomb'
        ]
        self._dangerous_commands = [
            'rm', 'mkfs', 'dd', 'shutdown', 'reboot', 'halt', 'init'
        ]

    def _validate_command_safety(self, cmd: str) -> None:
        if not self.safe_mode:
            return
        cmd_lower = cmd.lower()
        for pattern in self._dangerous_patterns:
            if pattern in cmd_lower:
                raise ValueError(
                    f"Unsafe command detected: '{pattern}' in '{cmd}'")
        for dangerous in self._dangerous_commands:
            if cmd_lower.strip().startswith(dangerous):
                raise ValueError(
                    f"Unsafe command detected: '{dangerous}' in '{cmd}'")

    def run(self, *parts: str, timeout: int = 30, cwd: Optional[str] = None) -> str:
        cmd = " ".join(parts)
        self._validate_command_safety(cmd)
        if self.dry_run:
            return f"[DRY RUN] {cmd}"
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd,
                check=False
            )
            return result.stdout.strip() + (("\n" + result.stderr.strip()) if result.stderr.strip() else "")
        except subprocess.TimeoutExpired as e:
            return f"Command timed out: {e}"

    def run_check(self, *parts: str, timeout: int = 30, cwd: Optional[str] = None) -> bool:
        cmd = " ".join(parts)
        self._validate_command_safety(cmd)
        if self.dry_run:
            return True
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd,
                check=False
            )
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            return False

    def write_file(self, path: str, content: str, mode: str = 'w', create_dirs: bool = True, permissions: Optional[int] = None) -> None:
        if self.dry_run:
            return
        dir_path = os.path.dirname(path)
        if create_dirs and dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        with open(path, mode) as f:
            f.write(content)
        if permissions is not None:
            os.chmod(path, permissions)
