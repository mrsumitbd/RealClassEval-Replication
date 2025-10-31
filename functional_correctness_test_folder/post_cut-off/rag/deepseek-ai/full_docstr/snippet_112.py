
import os
import time
from pathlib import Path
from typing import Optional, Tuple


class SessionResetHandler:
    """Handles detection and recovery from Claude session resets"""

    def __init__(self, log_func=None):
        """Initialize the handler
        Args:
            log_func: Optional logging function
        """
        self._log_func = log_func
        self._reset_command = None
        self._reset_time = None

    def check_for_reset_command(self, command: str) -> bool:
        """Check if a command is a session reset command"""
        return command.strip().lower() == "/clear"

    def mark_reset_detected(self, command: str) -> None:
        """Mark that a session reset has been detected"""
        self._reset_command = command
        self._reset_time = time.time()

    def is_reset_pending(self) -> bool:
        """Check if a session reset is pending"""
        return self._reset_time is not None

    def clear_reset_state(self) -> None:
        """Clear the reset state after handling"""
        self._reset_command = None
        self._reset_time = None

    def get_reset_info(self) -> Tuple[Optional[str], Optional[float]]:
        """Get information about the pending reset"""
        return (self._reset_command, self._reset_time)

    def find_reset_session_file(self, project_dir: Path, current_file: Path, max_wait: float = 10.0) -> Optional[Path]:
        """Find a new session file created after a reset
        Looks for JSONL files created after the reset time that contain
        <command-name>/clear</command-name> in the first few lines.
        Args:
            project_dir: Directory to search in
            current_file: Current JSONL file being monitored
            max_wait: Maximum time to wait in seconds
        Returns:
            Path to new JSONL file if found, None otherwise
        """
        if self._reset_time is None:
            return None

        start_time = time.time()
        while time.time() - start_time < max_wait:
            for file in project_dir.glob("*.jsonl"):
                if file == current_file:
                    continue
                if file.stat().st_mtime > self._reset_time and self._file_has_clear_command(file):
                    return file
            time.sleep(0.5)
        return None

    def _file_has_clear_command(self, file: Path) -> bool:
        """Check if a JSONL file starts with the /clear command"""
        try:
            with open(file, "r", encoding="utf-8") as f:
                first_line = f.readline()
                return "<command-name>/clear</command-name>" in first_line
        except (IOError, UnicodeDecodeError):
            return False
