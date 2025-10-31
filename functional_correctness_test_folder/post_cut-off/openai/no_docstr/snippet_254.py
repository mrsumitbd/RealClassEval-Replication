
import os
from datetime import datetime, timedelta
from typing import Optional


class TimeTracker:
    def __init__(self, history_dir: str):
        """
        Initialize the TimeTracker with the directory where history files are stored.
        """
        self.history_dir = history_dir

    def _get_character_history_file(self, character_id: str) -> str:
        """
        Return the full path to the history file for the given character.
        """
        # Use a simple naming convention: <character_id>.txt
        return os.path.join(self.history_dir, f"{character_id}.txt")

    def get_last_message_time(self, character_id: str) -> Optional[datetime]:
        """
        Read the history file for the character and return the most recent timestamp.
        If the file does not exist or contains no valid timestamps, return None.
        """
        history_file = self._get_character_history_file(character_id)
        if not os.path.isfile(history_file):
            return None

        last_time: Optional[datetime] = None
        with open(history_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    # Assume ISO 8601 format
                    ts = datetime.fromisoformat(line)
                except ValueError:
                    # Skip lines that cannot be parsed
                    continue
                if last_time is None or ts > last_time:
                    last_time = ts
        return last_time

    def format_time_elapsed(self, last_time: Optional[datetime], current_time: datetime) -> str:
        """
        Return a human‑readable string describing the time elapsed between
        last_time and current_time. If last_time is None, indicate that there
        is no previous message.
        """
        if last_time is None:
            return "No previous message"

        delta: timedelta = current_time - last_time
        if delta.total_seconds() < 0:
            # Future timestamp – treat as no previous message
            return "No previous message"

        days = delta.days
        seconds = delta.seconds

        parts = []
        if days > 0:
            parts.append(f"{days} day{'s' if days != 1 else ''}")
        if seconds >= 3600:
            hours = seconds // 3600
            parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
            seconds %= 3600
        if seconds >= 60:
            minutes = seconds // 60
            parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
            seconds %= 60
        if seconds > 0 or not parts:
            parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")

        return ", ".join(parts)

    def get_time_elapsed_prefix(self, character_id: str) -> str:
        """
        Return a prefix string that can be used in a message to indicate how
        long ago the last message from the character was sent.
        """
        last_time = self.get_last_message_time(character_id)
        now = datetime.now()
        elapsed = self.format_time_elapsed(last_time, now)
        return f"Last message was {elapsed}"
