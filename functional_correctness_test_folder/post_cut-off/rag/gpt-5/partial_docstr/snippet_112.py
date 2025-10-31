from pathlib import Path
from typing import Optional, Tuple, Callable
import time
import re


class SessionResetHandler:
    '''Handles detection and recovery from Claude session resets'''

    def __init__(self, log_func: Optional[Callable[[str], None]] = None):
        '''Initialize the handler
        Args:
            log_func: Optional logging function
        '''
        self._log: Callable[[str], None] = log_func if callable(
            log_func) else (lambda _: None)
        self._reset_pending: bool = False
        self._reset_command: Optional[str] = None
        self._reset_time: Optional[float] = None
        self._reset_patterns = (
            r'^\s*/clear\b',
            r'^\s*/reset\b',
            r'^\s*clear\b',
            r'^\s*/session-reset\b',
        )

    def check_for_reset_command(self, command: str) -> bool:
        '''Check if a command is a session reset command'''
        if not isinstance(command, str):
            return False
        cmd = command.strip().lower()
        for pat in self._reset_patterns:
            if re.search(pat, cmd):
                return True
        return False

    def mark_reset_detected(self, command: str) -> None:
        '''Mark that a session reset has been detected'''
        self._reset_pending = True
        self._reset_command = (command or '').strip()
        self._reset_time = time.time()
        self._log(
            f'Session reset detected: {self._reset_command!r} at {self._reset_time}')

    def is_reset_pending(self) -> bool:
        '''Check if a session reset is pending'''
        return bool(self._reset_pending and self._reset_time is not None)

    def clear_reset_state(self) -> None:
        '''Clear the reset state after handling'''
        self._log('Clearing session reset state')
        self._reset_pending = False
        self._reset_command = None
        self._reset_time = None

    def get_reset_info(self) -> Tuple[Optional[str], Optional[float]]:
        '''Get information about the pending reset'''
        return self._reset_command, self._reset_time

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
        if not self.is_reset_pending():
            return None
        if not isinstance(project_dir, Path):
            project_dir = Path(project_dir)
        if not isinstance(current_file, Path):
            current_file = Path(current_file)

        start = time.time()
        deadline = start + max_wait
        reset_time = self._reset_time or start

        self._log(
            f'Looking for new session file after reset time {reset_time} (wait up to {max_wait}s)')

        while time.time() <= deadline:
            try:
                candidates = []
                for path in project_dir.rglob('*.jsonl'):
                    if not path.is_file():
                        continue
                    if path.resolve() == current_file.resolve():
                        continue
                    try:
                        mtime = path.stat().st_mtime
                    except OSError:
                        continue
                    if mtime >= reset_time:
                        candidates.append((mtime, path))
                # Check newest files first
                candidates.sort(key=lambda x: x[0], reverse=True)

                for _, path in candidates:
                    if self._file_has_clear_command(path):
                        self._log(f'Found new session file: {path}')
                        return path
            except Exception as exc:
                self._log(f'Error while searching for session files: {exc!r}')
            time.sleep(0.25)

        self._log('No new session file found within wait period')
        return None

    def _file_has_clear_command(self, file: Path) -> bool:
        '''Check if a JSONL file starts with the /clear command'''
        try:
            with file.open('r', encoding='utf-8', errors='ignore') as fh:
                # Read and inspect the first few lines for a clear indication
                for i in range(12):
                    line = fh.readline()
                    if not line:
                        break
                    l = line.strip().lower()
                    if '/clear' in l:
                        return True
                    if '<command-name>' in l and '/clear' in l:
                        return True
                    if '"command-name"' in l and '/clear' in l:
                        return True
        except OSError:
            return False
        return False
