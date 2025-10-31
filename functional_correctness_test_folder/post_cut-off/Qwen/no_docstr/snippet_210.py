
import os
import subprocess
from typing import Optional


class Shell:

    def __init__(self, dry_run: bool = False, safe_mode: bool = True):
        self.dry_run = dry_run
        self.safe_mode = safe_mode

    def _validate_command_safety(self, cmd: str) -> None:
        if self.safe_mode:
            unsafe_chars = [';', '&', '|', '>', '<', '`', '$', '(', ')', '\\']
            if any(char in cmd for char in unsafe_chars):
                raise ValueError(f"Command contains unsafe characters: {cmd}")

    def run(self, *parts: str, timeout: int = 30, cwd: Optional[str] = None) -> str:
        cmd = ' '.join(parts)
        if self.safe_mode:
            self._validate_command_safety(cmd)
        if self.dry_run:
            print(f"Dry run: {cmd}")
            return ""
        try:
            result = subprocess.run(
                cmd, shell=True, check=True, timeout=timeout, cwd=cwd, capture_output=True, text=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Command failed with error: {e.stderr}")
            return e.stderr

    def run_check(self, *parts: str, timeout: int = 30, cwd: Optional[str] = None) -> bool:
        cmd = ' '.join(parts)
        if self.safe_mode:
            self._validate_command_safety(cmd)
        if self.dry_run:
            print(f"Dry run: {cmd}")
            return True
        try:
            subprocess.run(cmd, shell=True, check=True,
                           timeout=timeout, cwd=cwd)
            return True
        except subprocess.CalledProcessError:
            return False

    def write_file(self, path: str, content: str, mode: str = 'w', create_dirs: bool = True, permissions: Optional[int] = None) -> None:
        if create_dirs:
            os.makedirs(os.path.dirname(path), exist_ok=True)
        if self.dry_run:
            print(f"Dry run: Writing to {path} with content:\n{content}")
            return
        with open(path, mode) as file:
            file.write(content)
        if permissions is not None:
            os.chmod(path, permissions)
