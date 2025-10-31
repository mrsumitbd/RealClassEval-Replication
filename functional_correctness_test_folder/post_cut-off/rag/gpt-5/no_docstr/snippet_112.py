from __future__ import annotations

import time
import re
from pathlib import Path
from typing import Callable, Optional, Tuple


class SessionResetHandler:
    '''Handles detection and recovery from Claude session resets'''

    def __init__(self, log_func: Optional[Callable[[str], None]] = None):
        '''Initialize the handler
        Args:
            log_func: Optional logging function
        '''
        self._log: Callable[[str], None] = log_func if log_func is not None else (
            lambda _msg: None)
        self._reset_command: Optional[str] = None
        self._reset_time: Optional[float] = None

    def check_for_reset_command(self, command: str) -> bool:
        '''Check if a command is a session reset command'''
        if not command:
            return False
        cmd = command.strip().lower()
        reset_prefixes = ('/clear', '/reset', 'clear', 'reset')
        return any(cmd.startswith(p) for p in reset_prefixes)

    def mark_reset_detected(self, command: str) -> None:
        '''Mark that a session reset has been detected'''
        self._reset_command = command
        self._reset_time = time.time()
        self._log(
            f"Session reset detected: command={command!r} at {self._reset_time}")

    def is_reset_pending(self) -> bool:
        '''Check if a session reset is pending'''
        return self._reset_time is not None

    def clear_reset_state(self) -> None:
        '''Clear the reset state after handling'''
        self._log("Clearing session reset state")
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
            self._log("find_reset_session_file called with no pending reset")
            return None

        assert self._reset_time is not None  # for type checkers
        deadline = time.time() + max_wait
        tried = 0

        while time.time() < deadline:
            tried += 1
            try:
                candidates = sorted(
                    (p for p in project_dir.rglob('*.jsonl')
                     if p.resolve() != current_file.resolve()),
                    key=lambda p: p.stat().st_mtime,
                    reverse=True,
                )
            except Exception as exc:
                self._log(f"Error listing session files: {exc}")
                candidates = []

            for path in candidates:
                try:
                    st = path.stat()
                except FileNotFoundError:
                    continue
                except Exception as exc:
                    self._log(f"Error stat() on {path}: {exc}")
                    continue

                if st.st_mtime + 1e-6 < self._reset_time:
                    continue

                if st.st_size <= 0:
                    continue

                if self._file_has_clear_command(path):
                    self._log(
                        f"Found reset session file after {tried} scans: {path}")
                    return path

            time.sleep(0.2)

        self._log("No reset session file found within wait window")
        return None

    def _file_has_clear_command(self, file: Path) -> bool:
        '''Check if a JSONL file starts with the /clear command'''
        # Accept either explicit tag format or simple "/clear" presence near the start
        tag_pattern = re.compile(
            r'<\s*command-name\s*>\s*/clear\s*</\s*command-name\s*>', re.IGNORECASE)
        clear_pattern = re.compile(
            r'(^|\b|["\']:)\s*/clear(\b|["\':]|/|\\|\s|$)', re.IGNORECASE)

        try:
            with file.open('r', encoding='utf-8', errors='ignore') as fh:
                # Read a limited number of lines to avoid large file cost
                lines_to_check = 25
                buf_parts = []
                for _ in range(lines_to_check):
                    line = fh.readline()
                    if not line:
                        break
                    buf_parts.append(line)
                buf = ''.join(buf_parts)
        except Exception:
            return False

        if tag_pattern.search(buf):
            return True
        if clear_pattern.search(buf):
            return True
        return False
