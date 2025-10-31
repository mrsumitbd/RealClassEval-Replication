
import json
from pathlib import Path
from typing import Optional, Tuple
import time


class SessionResetHandler:
    '''Handles detection and recovery from Claude session resets'''

    def __init__(self, log_func=None):
        '''Initialize the handler
        Args:
            log_func: Optional logging function
        '''
        self._log_func = log_func
        self._reset_detected = False
        self._reset_command = None
        self._reset_time = None

    def check_for_reset_command(self, command: str) -> bool:
        '''Check if a command is a session reset command'''
        return command.strip().lower() == '/clear'

    def mark_reset_detected(self, command: str) -> None:
        '''Mark that a session reset has been detected'''
        self._reset_detected = True
        self._reset_command = command
        self._reset_time = time.time()

    def is_reset_pending(self) -> bool:
        return self._reset_detected

    def clear_reset_state(self) -> None:
        '''Clear the reset state after handling'''
        self._reset_detected = False
        self._reset_command = None
        self._reset_time = None

    def get_reset_info(self) -> Tuple[Optional[str], Optional[float]]:
        return (self._reset_command, self._reset_time)

    def find_reset_session_file(self, project_dir: Path, current_file: Path, max_wait: float = 10.0) -> Optional[Path]:
        start_time = time.time()
        while time.time() - start_time < max_wait:
            for file in project_dir.glob('*.jsonl'):
                if file != current_file and self._file_has_clear_command(file):
                    return file
            time.sleep(0.1)
        return None

    def _file_has_clear_command(self, file: Path) -> bool:
        '''Check if a JSONL file starts with the /clear command'''
        try:
            with open(file, 'r') as f:
                first_line = f.readline()
                if not first_line:
                    return False
                data = json.loads(first_line)
                return data.get('content', '').strip().lower() == '/clear'
        except (json.JSONDecodeError, IOError):
            return False
