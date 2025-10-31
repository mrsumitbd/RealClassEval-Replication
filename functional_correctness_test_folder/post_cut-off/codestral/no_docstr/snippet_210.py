
import os
import subprocess
from typing import Optional


class Shell:

    def __init__(self, dry_run: bool = False, safe_mode: bool = True):
        self.dry_run = dry_run
        self.safe_mode = safe_mode

    def _validate_command_safety(self, cmd: str) -> None:
        if self.safe_mode:
            unsafe_commands = ['rm', 'mv', 'cp', 'chmod', 'chown', 'dd',
                               'mkfs', 'fsck', 'shutdown', 'reboot', 'halt', 'init']
            for unsafe_cmd in unsafe_commands:
                if cmd.startswith(unsafe_cmd):
                    raise ValueError(f"Unsafe command: {cmd}")

    def run(self, *parts: str, timeout: int = 30, cwd: Optional[str] = None) -> str:
        cmd = ' '.join(parts)
        self._validate_command_safety(cmd)
        if self.dry_run:
            print(f"Dry run: {cmd}")
            return ""
        try:
            result = subprocess.run(cmd, shell=True, check=True, timeout=timeout,
                                    cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Command failed: {e.stderr}")

    def run_check(self, *parts: str, timeout: int = 30, cwd: Optional[str] = None) -> bool:
        try:
            self.run(*parts, timeout=timeout, cwd=cwd)
            return True
        except RuntimeError:
            return False

    def write_file(self, path: str, content: str, mode: str = 'w', create_dirs: bool = True, permissions: Optional[int] = None) -> None:
        if create_dirs:
            os.makedirs(os.path.dirname(path), exist_ok=True)
        if self.dry_run:
            print(f"Dry run: Writing to {path}")
            return
        with open(path, mode) as f:
            f.write(content)
        if permissions is not None:
            os.chmod(path, permissions)
