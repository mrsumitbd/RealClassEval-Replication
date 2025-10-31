
import os
import subprocess
import shlex
from typing import Optional


class Shell:

    def __init__(self, dry_run: bool = False, safe_mode: bool = True):
        self.dry_run = dry_run
        self.safe_mode = safe_mode

    def _validate_command_safety(self, cmd: str) -> None:
        if not self.safe_mode:
            return
        unsafe_chars = {';', '&', '|', '>', '<',
                        '`', '$', '(', ')', '{', '}', '[', ']'}
        for char in unsafe_chars:
            if char in cmd:
                raise ValueError(
                    f"Unsafe character '{char}' detected in command")

    def run(self, *parts: str, timeout: int = 30, cwd: Optional[str] = None) -> str:
        cmd = ' '.join(parts)
        self._validate_command_safety(cmd)
        if self.dry_run:
            return f"Dry run: {cmd}"
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                check=True,
                timeout=timeout,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return result.stdout
        except subprocess.TimeoutExpired:
            raise TimeoutError(f"Command timed out after {timeout} seconds")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Command failed with error: {e.stderr}")

    def run_check(self, *parts: str, timeout: int = 30, cwd: Optional[str] = None) -> bool:
        cmd = ' '.join(parts)
        self._validate_command_safety(cmd)
        if self.dry_run:
            return True
        try:
            subprocess.run(
                cmd,
                shell=True,
                check=True,
                timeout=timeout,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return True
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            return False

    def write_file(self, path: str, content: str, mode: str = 'w', create_dirs: bool = True, permissions: Optional[int] = None) -> None:
        if self.dry_run:
            print(f"Dry run: Writing to {path} with mode {mode}")
            return
        dirname = os.path.dirname(path)
        if create_dirs and dirname:
            os.makedirs(dirname, exist_ok=True)
        with open(path, mode) as f:
            f.write(content)
        if permissions is not None:
            os.chmod(path, permissions)
