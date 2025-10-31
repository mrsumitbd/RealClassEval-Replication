
from pathlib import Path
from typing import Optional, Tuple
import time
import os


class SessionResetHandler:
    '''Handles detection and recovery from Claude session resets'''

    def __init__(self, log_func=None):
        '''Initialize the handler
        Args:
            log_func: Optional logging function
        '''
        self._log = log_func
        self._reset_command: Optional[str] = None
        self._reset_time: Optional[float] = None

    def check_for_reset_command(self, command: str) -> bool:
        '''Check if a command is a session reset command'''
        if not command:
            return False
        cmd = command.strip().lower()
        # Common reset commands
        return "/clear" in cmd or "reset" in cmd

    def mark_reset_detected(self, command: str) -> None:
        '''Mark that a session reset has been detected'''
        self._reset_command = command
        self._reset_time = time.time()
        if self._log:
            self._log(f"Reset detected: {command} at {self._reset_time}")

    def is_reset_pending(self) -> bool:
        '''Check if a session reset is pending'''
        return self._reset_command is not None and self._reset_time is not None

    def clear_reset_state(self) -> None:
        '''Clear the reset state after handling'''
        if self._log:
            self._log("Clearing reset state")
        self._reset_command = None
        self._reset_time = None

    def get_reset_info(self) -> Tuple[Optional[str], Optional[float]]:
        '''Get information about the pending reset'''
        return self._reset_command, self._reset_time

    def find_reset_session_file(
        self,
        project_dir: Path,
        current_file: Path,
        max_wait: float = 10.0,
    ) -> Optional[Path]:
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
        if not self.is_reset_pending():
            return None

        start_time = time.time()
        reset_time = self._reset_time

        while time.time() - start_time < max_wait:
            # Find all JSONL files in project_dir
            candidates = sorted(
                (p for p in project_dir.rglob("*.jsonl") if p.is_file()),
                key=lambda p: p.stat().st_mtime,
            )
            for file_path in candidates:
                try:
                    mtime = file_path.stat().st_mtime
                except OSError:
                    continue
                if mtime <= reset_time:
                    continue
                if file_path.resolve() == current_file.resolve():
                    continue
                if self._file_has_clear_command(file_path):
                    if self._log:
                        self._log(f"Found reset session file: {file_path}")
                    return file_path
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
                    if "/clear" in line.lower():
                        return True
        except Exception:
            pass
        return False
