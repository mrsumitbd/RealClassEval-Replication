
from typing import Optional, Tuple
from pathlib import Path
import time


class SessionResetHandler:

    def __init__(self, log_func=None):
        self._reset_pending = False
        self._reset_command = None
        self._reset_time = None
        self._log_func = log_func

    def check_for_reset_command(self, command: str) -> bool:
        if "reset" in command.lower():
            self.mark_reset_detected(command)
            return True
        return False

    def mark_reset_detected(self, command: str) -> None:
        self._reset_pending = True
        self._reset_command = command
        self._reset_time = time.time()
        if self._log_func:
            self._log_func(f"Reset detected: {command}")

    def is_reset_pending(self) -> bool:
        return self._reset_pending

    def clear_reset_state(self) -> None:
        self._reset_pending = False
        self._reset_command = None
        self._reset_time = None

    def get_reset_info(self) -> Tuple[Optional[str], Optional[float]]:
        return (self._reset_command, self._reset_time)

    def find_reset_session_file(self, project_dir: Path, current_file: Path, max_wait: float = 10.0) -> Optional[Path]:
        start_time = time.time()
        while time.time() - start_time < max_wait:
            for file in project_dir.rglob("*.session"):
                if self._file_has_clear_command(file):
                    return file
            time.sleep(0.1)
        return None

    def _file_has_clear_command(self, file: Path) -> bool:
        try:
            with open(file, 'r') as f:
                content = f.read()
                return "clear" in content.lower()
        except:
            return False
