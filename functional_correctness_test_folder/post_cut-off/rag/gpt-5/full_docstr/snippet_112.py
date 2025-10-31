from pathlib import Path
from typing import Optional, Tuple, Callable, Set
import time
import os


class SessionResetHandler:
    '''Handles detection and recovery from Claude session resets'''

    def __init__(self, log_func: Optional[Callable[[str], None]] = None):
        '''Initialize the handler
        Args:
            log_func: Optional logging function
        '''
        self._log: Callable[[str], None] = log_func if log_func is not None else (
            lambda msg: None)
        self._reset_pending: bool = False
        self._last_reset_command: Optional[str] = None
        self._reset_time: Optional[float] = None
        self._reset_commands: Set[str] = {
            '/reset',
            '/reset_session',
            '/reset-session',
            '/new',
            '/new_session',
            '/new-session',
            '/restart',
            '/start_new_session',
            '/start-new-session',
        }

    def check_for_reset_command(self, command: str) -> bool:
        '''Check if a command is a session reset command'''
        if not command:
            return False
        cmd = command.strip().lower()
        # Handle potential XML-wrapped command like <command-name>/reset</command-name>
        if cmd.startswith('<command-name>') and cmd.endswith('</command-name>'):
            cmd = cmd.replace('<command-name>',
                              '').replace('</command-name>', '').strip()
        if ' ' in cmd:
            cmd = cmd.split()[0]
        return cmd in self._reset_commands

    def mark_reset_detected(self, command: str) -> None:
        '''Mark that a session reset has been detected'''
        self._reset_pending = True
        self._last_reset_command = command.strip() if command else None
        self._reset_time = time.time()
        self._log(
            f'Session reset detected via command: {self._last_reset_command}')

    def is_reset_pending(self) -> bool:
        '''Check if a session reset is pending'''
        return self._reset_pending

    def clear_reset_state(self) -> None:
        '''Clear the reset state after handling'''
        self._log('Clearing session reset state')
        self._reset_pending = False
        self._last_reset_command = None
        self._reset_time = None

    def get_reset_info(self) -> Tuple[Optional[str], Optional[float]]:
        '''Get information about the pending reset'''
        return self._last_reset_command, self._reset_time

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
        if not self._reset_pending or self._reset_time is None:
            return None
        if not project_dir.exists():
            return None

        deadline = time.monotonic() + max_wait
        last_seen_candidates: Set[Path] = set()

        while time.monotonic() < deadline:
            candidates = []
            try:
                for path in project_dir.rglob('*.jsonl'):
                    if current_file and path.resolve() == current_file.resolve():
                        continue
                    try:
                        st = path.stat()
                    except OSError:
                        continue
                    if st.st_size <= 0:
                        continue
                    if self._reset_time is not None and st.st_mtime >= self._reset_time:
                        candidates.append((st.st_mtime, path))
            except Exception:
                # Ignore transient filesystem errors
                pass

            # Prefer newest first
            candidates.sort(reverse=True)

            for _, path in candidates:
                if path in last_seen_candidates:
                    continue
                if self._file_has_clear_command(path):
                    self._log(f'Found new session file after reset: {path}')
                    return path
                last_seen_candidates.add(path)

            time.sleep(0.2)

        return None

    def _file_has_clear_command(self, file: Path) -> bool:
        '''Check if a JSONL file starts with the /clear command'''
        marker = '<command-name>/clear</command-name>'
        try:
            with file.open('r', encoding='utf-8', errors='ignore') as fh:
                for _ in range(10):
                    line = fh.readline()
                    if not line:
                        break
                    if marker in line:
                        return True
        except OSError:
            return False
        return False
