from pathlib import Path
from typing import Optional, Tuple, Callable, Iterable
import time
import os


class SessionResetHandler:
    '''Handles detection and recovery from Claude session resets'''

    def __init__(self, log_func: Optional[Callable[[str], None]] = None):
        '''Initialize the handler
        Args:
            log_func: Optional logging function
        '''
        self._log = log_func
        self._reset_pending: bool = False
        self._reset_time: Optional[float] = None
        self._reset_command: Optional[str] = None

    def _logf(self, msg: str) -> None:
        if self._log:
            try:
                self._log(msg)
            except Exception:
                pass

    def check_for_reset_command(self, command: str) -> bool:
        '''Check if a command is a session reset command'''
        if command is None:
            return False
        cmd = command.strip().lower()
        if not cmd:
            return False
        if cmd.startswith("/"):
            cmd = cmd[1:]
        return cmd in {"clear", "reset", "new", "newsession", "new-session"}

    def mark_reset_detected(self, command: str) -> None:
        '''Mark that a session reset has been detected'''
        self._reset_pending = True
        self._reset_command = command
        self._reset_time = time.time()
        self._logf(
            f"Session reset detected via command: {command!r} at {self._reset_time}")

    def is_reset_pending(self) -> bool:
        '''Check if a session reset is pending'''
        return self._reset_pending

    def clear_reset_state(self) -> None:
        '''Clear the reset state after handling'''
        self._reset_pending = False
        self._reset_time = None
        self._reset_command = None
        self._logf("Session reset state cleared")

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
        if not self._reset_pending or self._reset_time is None:
            self._logf("No reset pending; not searching for new session file")
            return None

        start = time.time()
        deadline = start + max_wait

        project_dir = Path(project_dir)
        current_file = Path(current_file)

        def file_time(p: Path) -> float:
            try:
                st = p.stat()
                t_candidates: Iterable[float] = [
                    st.st_mtime, getattr(st, "st_ctime", st.st_mtime)]
                bt = getattr(st, "st_birthtime", None)
                if bt:
                    t_candidates = list(t_candidates) + [bt]
                return max(t_candidates)
            except Exception:
                return 0.0

        while time.time() <= deadline:
            if not project_dir.exists():
                self._logf(f"Project dir does not exist: {project_dir}")
                time.sleep(0.25)
                continue

            candidates = []
            try:
                for p in project_dir.glob("*.jsonl"):
                    if p.resolve() == current_file.resolve():
                        continue
                    t = file_time(p)
                    if t >= self._reset_time:
                        candidates.append((t, p))
            except Exception:
                pass

            candidates.sort(key=lambda x: x[0], reverse=True)

            for _, p in candidates:
                if self._file_has_clear_command(p):
                    self._logf(f"Found new reset session file: {p}")
                    return p

            time.sleep(0.25)

        self._logf("No new session file found within wait window")
        return None

    def _file_has_clear_command(self, file: Path) -> bool:
        '''Check if a JSONL file starts with the /clear command'''
        try:
            with open(file, "r", encoding="utf-8", errors="ignore") as f:
                for i, line in enumerate(f):
                    if i > 50:
                        break
                    s = line.strip().lower()
                    if "<command-name>/clear</command-name>" in s:
                        return True
                    if "/clear" in s or '"command":"clear"' in s or '"name":"/clear"' in s:
                        return True
            return False
        except Exception:
            return False
