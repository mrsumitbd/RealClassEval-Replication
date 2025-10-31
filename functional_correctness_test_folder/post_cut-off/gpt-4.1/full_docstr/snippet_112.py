
from typing import Optional, Tuple
from pathlib import Path
import time
import os


class SessionResetHandler:
    '''Handles detection and recovery from Claude session resets'''

    RESET_COMMANDS = {"/reset", "/clear",
                      "/restart", "reset session", "clear session"}

    def __init__(self, log_func=None):
        '''Initialize the handler
        Args:
            log_func: Optional logging function
        '''
        self._log = log_func
        self._reset_pending = False
        self._reset_command = None
        self._reset_time = None

    def check_for_reset_command(self, command: str) -> bool:
        '''Check if a command is a session reset command'''
        cmd = command.strip().lower()
        for reset_cmd in self.RESET_COMMANDS:
            if cmd == reset_cmd or cmd.startswith(reset_cmd + " "):
                return True
        return False

    def mark_reset_detected(self, command: str) -> None:
        '''Mark that a session reset has been detected'''
        self._reset_pending = True
        self._reset_command = command
        self._reset_time = time.time()
        if self._log:
            self._log(
                f"Session reset detected: '{command}' at {self._reset_time}")

    def is_reset_pending(self) -> bool:
        '''Check if a session reset is pending'''
        return self._reset_pending

    def clear_reset_state(self) -> None:
        '''Clear the reset state after handling'''
        self._reset_pending = False
        self._reset_command = None
        self._reset_time = None

    def get_reset_info(self) -> Tuple[Optional[str], Optional[float]]:
        '''Get information about the pending reset'''
        return (self._reset_command, self._reset_time)

    def find_reset_session_file(self, project_dir: Path, current_file: Path, max_wait: float = 10.0) -> Optional[Path]:
        '''Find a new session file created after a reset
        Looks for JSONL files created after the reset time that contain
        <command-name>/clear</command-name> in the first few lines.
        Args:
            project_dir: Directory to search in
            current_file: Current JSONL file being monitored
            max_wait: Maximum time to wait in seconds
        Returns:
            Path to new JSONL file if found, None otherwise
        '''
        if not self._reset_time:
            return None

        start_time = time.time()
        checked_files = set()
        while time.time() - start_time < max_wait:
            jsonl_files = sorted(
                [f for f in project_dir.glob("*.jsonl") if f != current_file],
                key=lambda f: f.stat().st_mtime,
                reverse=True
            )
            for f in jsonl_files:
                if f in checked_files:
                    continue
                try:
                    mtime = f.stat().st_mtime
                except Exception:
                    continue
                if mtime < self._reset_time:
                    continue
                if self._file_has_clear_command(f):
                    if self._log:
                        self._log(f"Found reset session file: {f}")
                    return f
                checked_files.add(f)
            time.sleep(0.5)
        return None

    def _file_has_clear_command(self, file: Path) -> bool:
        '''Check if a JSONL file starts with the /clear command'''
        try:
            with file.open("r", encoding="utf-8") as f:
                for _ in range(5):
                    line = f.readline()
                    if not line:
                        break
                    if "<command-name>/clear</command-name>" in line:
                        return True
        except Exception:
            pass
        return False
