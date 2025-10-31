
from typing import Optional, Tuple
from pathlib import Path
import time


class SessionResetHandler:

    def __init__(self, log_func=None):
        self._log_func = log_func
        self._reset_pending = False
        self._reset_command = None
        self._reset_time = None

    def check_for_reset_command(self, command: str) -> bool:
        if command.strip().lower() in {"reset", "clear session", "restart session"}:
            return True
        return False

    def mark_reset_detected(self, command: str) -> None:
        self._reset_pending = True
        self._reset_command = command
        self._reset_time = time.time()
        if self._log_func:
            self._log_func(
                f"Session reset detected: '{command}' at {self._reset_time}")

    def is_reset_pending(self) -> bool:
        return self._reset_pending

    def clear_reset_state(self) -> None:
        self._reset_pending = False
        self._reset_command = None
        self._reset_time = None
        if self._log_func:
            self._log_func("Session reset state cleared.")

    def get_reset_info(self) -> Tuple[Optional[str], Optional[float]]:
        return (self._reset_command, self._reset_time)

    def find_reset_session_file(self, project_dir: Path, current_file: Path, max_wait: float = 10.0) -> Optional[Path]:
        start_time = time.time()
        while time.time() - start_time < max_wait:
            for file in project_dir.glob("**/*"):
                if file.is_file() and file != current_file:
                    if self._file_has_clear_command(file):
                        if self._log_func:
                            self._log_func(f"Reset session file found: {file}")
                        return file
            time.sleep(0.5)
        if self._log_func:
            self._log_func("No reset session file found within wait time.")
        return None

    def _file_has_clear_command(self, file: Path) -> bool:
        try:
            with file.open("r", encoding="utf-8") as f:
                for line in f:
                    if self.check_for_reset_command(line):
                        return True
        except Exception:
            pass
        return False
