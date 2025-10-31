
from pathlib import Path
from typing import Optional, Tuple
import time
import re


class SessionResetHandler:
    """
    Handles detection and management of a session reset command.
    """

    def __init__(self, log_func=None):
        """
        Initialize the handler.

        :param log_func: Optional callable that accepts a string for logging.
        """
        self._log_func = log_func
        self._reset_command: Optional[str] = None
        self._reset_time: Optional[float] = None

    def check_for_reset_command(self, command: str) -> bool:
        """
        Determine whether the supplied command is a reset command.

        :param command: The command string to evaluate.
        :return: True if the command is a reset command, False otherwise.
        """
        if command is None:
            return False
        return command.strip().lower() == "reset"

    def mark_reset_detected(self, command: str) -> None:
        """
        Record that a reset command has been detected.

        :param command: The reset command string.
        """
        self._reset_command = command
        self._reset_time = time.time()
        if self._log_func:
            self._log_func(f"Reset detected: {command} at {self._reset_time}")

    def is_reset_pending(self) -> bool:
        """
        Check whether a reset has been detected and is pending.

        :return: True if a reset is pending, False otherwise.
        """
        return self._reset_command is not None

    def clear_reset_state(self) -> None:
        """
        Clear any stored reset state.
        """
        if self._log_func:
            self._log_func("Clearing reset state.")
        self._reset_command = None
        self._reset_time = None

    def get_reset_info(self) -> Tuple[Optional[str], Optional[float]]:
        """
        Retrieve the stored reset command and its timestamp.

        :return: A tuple of (reset_command, reset_time).
        """
        return self._reset_command, self._reset_time

    def find_reset_session_file(
        self,
        project_dir: Path,
        current_file: Path,
        max_wait: float = 10.0,
    ) -> Optional[Path]:
        """
        Search for a file in the project directory that contains a clear command.

        The search will continue until a file is found or the max_wait time is exceeded.

        :param project_dir: The root directory of the project.
        :param current_file: The file currently being processed (used to skip).
        :param max_wait: Maximum time in seconds to wait for a file to appear.
        :return: Path to the file containing a clear command, or None if not found.
        """
        start = time.time()
        while time.time() - start < max_wait:
            for candidate in project_dir.rglob("*"):
                if candidate.is_file() and candidate != current_file:
                    if self._file_has_clear_command(candidate):
                        return candidate
            time.sleep(0.1)
        return None

    def _file_has_clear_command(self, file: Path) -> bool:
        """
        Determine whether the given file contains a clear command.

        The check is case-insensitive and looks for the exact word "clear" or "reset"
        on a line by itself.

        :param file: Path to the file to inspect.
        :return: True if the file contains a clear command, False otherwise.
        """
        try:
            with file.open("r", encoding="utf-8") as f:
                for line in f:
                    stripped = line.strip().lower()
                    if stripped in {"clear", "reset"}:
                        return True
        except (OSError, UnicodeDecodeError):
            # If the file cannot be read, treat it as not containing a clear command.
            pass
        return False
