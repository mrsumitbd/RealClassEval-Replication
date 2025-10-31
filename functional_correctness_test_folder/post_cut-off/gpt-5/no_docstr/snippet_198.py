from typing import Optional, Dict, Any
import subprocess
import time
import os
import sys


class ShortcutsCommand:

    def __init__(self):
        self.last_result: Optional[Dict[str, Any]] = None

    def run(self, shell: Optional[str] = None) -> int:
        start = time.time()
        if shell is None or not isinstance(shell, str) or not shell.strip():
            result = {
                "command": "",
                "returncode": 0,
                "stdout": "",
                "stderr": "",
                "start_time": start,
                "end_time": start,
                "duration": 0.0,
                "error": None,
            }
            self.last_result = result
            self._print_result(result)
            return 0

        try:
            proc = subprocess.run(
                shell,
                shell=True,
                capture_output=True,
                text=True,
                check=False,
                env=os.environ.copy(),
            )
            end = time.time()
            result = {
                "command": shell,
                "returncode": proc.returncode,
                "stdout": proc.stdout or "",
                "stderr": proc.stderr or "",
                "start_time": start,
                "end_time": end,
                "duration": end - start,
                "error": None,
            }
        except Exception as exc:
            end = time.time()
            result = {
                "command": shell,
                "returncode": 1,
                "stdout": "",
                "stderr": "",
                "start_time": start,
                "end_time": end,
                "duration": end - start,
                "error": repr(exc),
            }

        self.last_result = result
        self._print_result(result)
        return int(result.get("returncode", 1))

    def _print_result(self, result: dict) -> None:
        out = sys.stdout
        err = sys.stderr

        cmd = result.get("command", "")
        rc = result.get("returncode", 1)
        stdout_data = result.get("stdout", "")
        stderr_data = result.get("stderr", "")
        error_obj = result.get("error", None)
        duration = result.get("duration", 0.0)

        if cmd:
            print(f"$ {cmd}", file=out)

        if stdout_data:
            print(stdout_data, end="" if stdout_data.endswith(
                "\n") else "\n", file=out)

        if stderr_data:
            print(stderr_data, end="" if stderr_data.endswith(
                "\n") else "\n", file=err)

        if error_obj is not None:
            print(f"[error] {error_obj}", file=err)

        print(f"[exit {rc}] ({duration:.3f}s)", file=out)

        try:
            out.flush()
        except Exception:
            pass
        try:
            err.flush()
        except Exception:
            pass
