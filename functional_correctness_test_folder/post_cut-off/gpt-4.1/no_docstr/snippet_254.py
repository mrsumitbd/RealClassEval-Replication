
import os
from datetime import datetime
from typing import Optional


class TimeTracker:

    def __init__(self, history_dir: str):
        self.history_dir = history_dir

    def _get_character_history_file(self, character_id: str) -> str:
        return os.path.join(self.history_dir, f"{character_id}.txt")

    def get_last_message_time(self, character_id: str) -> Optional[datetime]:
        file_path = self._get_character_history_file(character_id)
        if not os.path.exists(file_path):
            return None
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                if not lines:
                    return None
                last_line = lines[-1].strip()
                if not last_line:
                    return None
                # Assume the timestamp is the first part of the line, ISO format
                timestamp_str = last_line.split()[0]
                try:
                    last_time = datetime.fromisoformat(timestamp_str)
                    return last_time
                except Exception:
                    return None
        except Exception:
            return None

    def format_time_elapsed(self, last_time: Optional[datetime], current_time: datetime) -> str:
        if last_time is None:
            return "No previous message"
        delta = current_time - last_time
        seconds = int(delta.total_seconds())
        if seconds < 60:
            return f"{seconds} seconds ago"
        minutes = seconds // 60
        if minutes < 60:
            return f"{minutes} minutes ago"
        hours = minutes // 60
        if hours < 24:
            return f"{hours} hours ago"
        days = hours // 24
        return f"{days} days ago"

    def get_time_elapsed_prefix(self, character_id: str) -> str:
        last_time = self.get_last_message_time(character_id)
        now = datetime.now()
        elapsed = self.format_time_elapsed(last_time, now)
        return f"[{elapsed}]"
