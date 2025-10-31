
from typing import Optional, Tuple
from pathlib import Path
import time
import json


class SessionResetHandler:
    '''Handles detection and recovery from Claude session resets'''
    RESET_COMMANDS = {"/clear", "/reset", "/restart", "/startover"}

    def __init__(self, log_func=None):
        '''Initialize the handler
        Args:
            log_func: Optional logging function
        '''
        self.log_func = log_func
        self._reset_pending = False
        self._reset_command = None
        self._reset_time = None

    def check_for_reset_command(self, command: str) -> bool:
        '''Check if a command is a session reset command'''
        if not isinstance(command, str):
            return False
        cmd = command.strip().lower()
        if cmd in self.RESET_COMMANDS:
            return True
        return False

    def mark_reset_detected(self, command: str) -> None:
        '''Mark that a session reset has been detected'''
        self._reset_pending = True
        self._reset_command = command
        self._reset_time = time.time()
        if self.log_func:
            self.log_func(f"Session reset detected: {command}")

    def is_reset_pending(self) -> bool:
        return self._reset_pending

    def clear_reset_state(self) -> None:
        '''Clear the reset state after handling'''
        self._reset_pending = False
        self._reset_command = None
        self._reset_time = None

    def get_reset_info(self) -> Tuple[Optional[str], Optional[float]]:
        return (self._reset_command, self._reset_time)

    def find_reset_session_file(self, project_dir: Path, current_file: Path, max_wait: float = 10.0) -> Optional[Path]:
        '''
        Look for a new session file in project_dir that is not current_file,
        and that starts with a /clear command. Wait up to max_wait seconds.
        '''
        start_time = time.time()
        while time.time() - start_time < max_wait:
            files = sorted(project_dir.glob("*.jsonl"),
                           key=lambda f: f.stat().st_mtime, reverse=True)
            for file in files:
                if file == current_file:
                    continue
                if self._file_has_clear_command(file):
                    if self.log_func:
                        self.log_func(f"Found reset session file: {file}")
                    return file
            time.sleep(0.5)
        return None

    def _file_has_clear_command(self, file: Path) -> bool:
        '''Check if a JSONL file starts with the /clear command'''
        try:
            with file.open("r", encoding="utf-8") as f:
                first_line = f.readline()
                if not first_line:
                    return False
                try:
                    obj = json.loads(first_line)
                except Exception:
                    return False
                # Assume the command is in a field called "text" or "content"
                text = obj.get("text") or obj.get("content")
                if not text:
                    return False
                return self.check_for_reset_command(text)
        except Exception:
            return False
