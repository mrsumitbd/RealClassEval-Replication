
import os
import time
from pathlib import Path
from typing import Optional, Tuple, Callable


class SessionResetHandler:
    '''Handles detection and recovery from Claude session resets'''

    def __init__(self, log_func: Optional[Callable] = None):
        '''Initialize the handler
        Args:
            log_func: Optional logging function
        '''
        self.log_func = log_func
        self.reset_detected = False
        self.reset_command = None
        self.reset_time = None

    def check_for_reset_command(self, command: str) -> bool:
        '''Check if a command is a session reset command'''
        # For this example, we assume '/clear' is the reset command
        return command.strip().lower() == '/clear'

    def mark_reset_detected(self, command: str) -> None:
        '''Mark that a session reset has been detected'''
        self.reset_detected = True
        self.reset_command = command
        self.reset_time = time.time()
        if self.log_func:
            self.log_func(f"Session reset detected: {command}")

    def is_reset_pending(self) -> bool:
        '''Check if a session reset is pending'''
        return self.reset_detected

    def clear_reset_state(self) -> None:
        '''Clear the reset state after handling'''
        self.reset_detected = False
        self.reset_command = None
        self.reset_time = None

    def get_reset_info(self) -> Tuple[Optional[str], Optional[float]]:
        '''Get information about the pending reset'''
        return self.reset_command, self.reset_time

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
        start_time = time.time()
        while time.time() - start_time < max_wait:
            for file in project_dir.iterdir():
                if file.is_file() and file.suffix == '.jsonl' and file != current_file:
                    if file.stat().st_mtime > self.reset_time and self._file_has_clear_command(file):
                        return file
            time.sleep(0.1)
        return None

    def _file_has_clear_command(self, file: Path) -> bool:
        '''Check if a JSONL file starts with the /clear command'''
        try:
            with open(file, 'r') as f:
                for _ in range(10):  # Check first 10 lines
                    line = f.readline().strip()
                    if '/clear' in line:
                        return True
        except Exception as e:
            if self.log_func:
                self.log_func(f"Error reading file {file}: {e}")
        return False
