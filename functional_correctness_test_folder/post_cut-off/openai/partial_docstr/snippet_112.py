
from pathlib import Path
from typing import Optional, Tuple
import time
import json


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
        self._reset_detected: bool = False

    def _log_msg(self, msg: str) -> None:
        if self._log:
            try:
                self._log(msg)
            except Exception:
                pass  # ignore logging errors

    def check_for_reset_command(self, command: str) -> bool:
        '''Check if a command is a session reset command'''
        if not command:
            return False
        cmd = command.strip().lower()
        return cmd in {"/reset", "/clear", "reset", "clear"}

    def mark_reset_detected(self, command: str) -> None:
        '''Mark that a session reset has been detected'''
        if self.check_for_reset_command(command):
            self._reset_command = command.strip()
            self._reset_time = time.time()
            self._reset_detected = True
            self._log_msg(f"Session reset detected: {self._reset_command}")

    def is_reset_pending(self) -> bool:
        '''Return True if a reset has been detected and not yet cleared'''
        return self._reset_detected

    def clear_reset_state(self) -> None:
        '''Clear the reset state after handling'''
        if self._reset_detected:
            self._log_msg("Clearing reset state")
        self._reset_command = None
        self._reset_time = None
        self._reset_detected = False

    def get_reset_info(self) -> Tuple[Optional[str], Optional[float]]:
        '''Return the reset command and timestamp, if any'''
        return self._reset_command, self._reset_time

    def find_reset_session_file(
        self, project_dir: Path, current_file: Path, max_wait: float = 10.0
    ) -> Optional[Path]:
        '''Find a JSONL file in the project that starts with a clear command.
        Waits up to max_wait seconds for such a file to appear.
        '''
        start = time.time()
        while time.time() - start <= max_wait:
            for file in project_dir.rglob("*.jsonl"):
                if file.resolve() == current_file.resolve():
                    continue
                try:
                    if self._file_has_clear_command(file):
                        self._log_msg(f"Found reset session file: {file}")
                        return file
                except Exception:
                    continue
            time.sleep(0.5)
        self._log_msg("No reset session file found within timeout")
        return None

    def _file_has_clear_command(self, file: Path) -> bool:
        '''Check if a JSONL file starts with the /clear command'''
        try:
            with file.open("r", encoding="utf-8") as f:
                first_line = f.readline()
                if not first_line:
                    return False
                # JSONL lines are JSON objects; the command might be in a field
                # Try to parse as JSON and look for a "command" key
                try:
                    obj = json.loads(first_line)
                    cmd = str(obj.get("command", "")).strip().lower()
                    return cmd in {"/reset", "/clear", "reset", "clear"}
                except json.JSONDecodeError:
                    # Fallback: check raw line
                    return first_line.strip().lower().startswith(("/reset", "/clear"))
        except FileNotFoundError:
            return False
        except Exception:
            return False
