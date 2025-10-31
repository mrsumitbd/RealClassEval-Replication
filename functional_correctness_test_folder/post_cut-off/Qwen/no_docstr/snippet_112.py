
from typing import Optional, Tuple
from pathlib import Path
import time


class SessionResetHandler:

    def __init__(self, log_func=None):
        self.log_func = log_func
        self.reset_detected = False
        self.reset_command = None
        self.reset_time = None

    def check_for_reset_command(self, command: str) -> bool:
        if "RESET_SESSION" in command:
            self.mark_reset_detected(command)
            return True
        return False

    def mark_reset_detected(self, command: str) -> None:
        self.reset_detected = True
        self.reset_command = command
        self.reset_time = time.time()
        if self.log_func:
            self.log_func(f"Reset command detected: {command}")

    def is_reset_pending(self) -> bool:
        return self.reset_detected

    def clear_reset_state(self) -> None:
        self.reset_detected = False
        self.reset_command = None
        self.reset_time = None

    def get_reset_info(self) -> Tuple[Optional[str], Optional[float]]:
        return self.reset_command, self.reset_time

    def find_reset_session_file(self, project_dir: Path, current_file: Path, max_wait: float = 10.0) -> Optional[Path]:
        start_time = time.time()
        while time.time() - start_time < max_wait:
            for file in project_dir.iterdir():
                if file != current_file and file.suffix == '.session' and self._file_has_clear_command(file):
                    return file
            time.sleep(0.1)
        return None

    def _file_has_clear_command(self, file: Path) -> bool:
        try:
            with file.open('r') as f:
                for line in f:
                    if "CLEAR_SESSION" in line:
                        return True
        except IOError:
            pass
        return False
