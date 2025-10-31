
import subprocess
import os
from typing import Optional


class Shell:

    def __init__(self, dry_run: bool = False, safe_mode: bool = True):
        self.dry_run = dry_run
        self.safe_mode = safe_mode

    def _validate_command_safety(self, cmd: str) -> None:
        if self.safe_mode:
            forbidden_commands = ['rm', 'mkfs', 'dd', 'shutdown', 'reboot']
            for forbidden_command in forbidden_commands:
                if forbidden_command in cmd:
                    raise ValueError(
                        f"Command '{cmd}' is not allowed in safe mode")

    def run(self, *parts: str, timeout: int = 30, cwd: Optional[str] = None) -> str:
        cmd = ' '.join(parts)
        self._validate_command_safety(cmd)
        if self.dry_run:
            print(f"Would run: {cmd}")
            return ""
        try:
            result = subprocess.run(cmd, shell=True, check=False, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, timeout=timeout, cwd=cwd)
            return result.stdout.decode('utf-8')
        except subprocess.TimeoutExpired:
            raise TimeoutError(
                f"Command '{cmd}' timed out after {timeout} seconds")

    def run_check(self, *parts: str, timeout: int = 30, cwd: Optional[str] = None) -> bool:
        cmd = ' '.join(parts)
        self._validate_command_safety(cmd)
        if self.dry_run:
            print(f"Would run: {cmd}")
            return True
        try:
            subprocess.run(cmd, shell=True, check=True,
                           timeout=timeout, cwd=cwd)
            return True
        except subprocess.CalledProcessError:
            return False
        except subprocess.TimeoutExpired:
            raise TimeoutError(
                f"Command '{cmd}' timed out after {timeout} seconds")

    def write_file(self, path: str, content: str, mode: str = 'w', create_dirs: bool = True, permissions: Optional[int] = None) -> None:
        if create_dirs:
            dir_path = os.path.dirname(path)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)
        if self.dry_run:
            print(f"Would write to file: {path}")
        else:
            with open(path, mode) as f:
                f.write(content)
            if permissions is not None:
                os.chmod(path, permissions)
