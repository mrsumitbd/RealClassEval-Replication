
import json
import time
from pathlib import Path
from typing import Optional, Tuple


class SessionResetHandler:
    '''Handles detection and recovery from Claude session resets'''

    def __init__(self, log_func=None):
        '''Initialize the handler
        Args:
            log_func: Optional logging function
        '''
        self.log_func = log_func
        self._reset_command: Optional[str] = None
        self._reset_time: Optional[float] = None

    def _log(self, msg: str) -> None:
        if self.log_func:
            try:
                self.log_func(msg)
            except Exception:
                # ignore logging errors
                pass

    def check_for_reset_command(self, command: str) -> bool:
        '''Check if a command is a session reset command'''
        if not command:
            return False
        cmd = command.strip().lower()
        # Common reset commands for Claude
        return cmd.startswith('/reset') or cmd.startswith('/clear')

    def mark_reset_detected(self, command: str) -> None:
        '''Mark that a session reset has been detected'''
        self._reset_command = command
        self._reset_time = time.time()
        self._log(f"Session reset detected: {command!r} at {self._reset_time}")

    def is_reset_pending(self) -> bool:
        '''Check if a session reset is pending'''
        return self._reset_command is not None

    def clear_reset_state(self) -> None:
        '''Clear the reset state after handling'''
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
            self._log("No reset pending; cannot find reset session file")
            return None

        reset_time = self._reset_time
        if reset_time is None:
            return None

        start = time.time()
        while time.time() - start < max_wait:
            for file in project_dir.rglob("*.jsonl"):
                if file.resolve() == current_file.resolve():
                    continue
                try:
                    mtime = file.stat().st_mtime
                except OSError:
                    continue
                if mtime <= reset_time:
                    continue
                if self._file_has_clear_command(file):
                    self._log(f"Found reset session file: {file}")
                    return file
            time.sleep(0.5)
        self._log("No reset session file found within timeout")
        return None

    def _file_has_clear_command(self, file: Path) -> bool:
        '''Check if a JSONL file starts with the /clear command'''
        try:
            with file.open("r", encoding="utf-8") as fp:
                for _ in range(5):
                    line = fp.readline()
                    if not line:
                        break
                    line_strip = line.strip()
                    if not line_strip:
                        continue
                    # Try JSON parsing
                    try:
                        data = json.loads(line_strip)
                        cmd = data.get("command", "").strip().lower()
                        if cmd == "/clear":
                            return True
                    except json.JSONDecodeError:
                        # Fallback: simple substring check
                        if "/clear" in line_strip.lower():
                            return True
        except Exception:
            # ignore read errors
            pass
        return False
