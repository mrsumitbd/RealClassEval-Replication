
import os
from datetime import datetime
from typing import Optional


class TimeTracker:

    def __init__(self, history_dir: str):
        self.history_dir = history_dir
        os.makedirs(history_dir, exist_ok=True)

    def _get_character_history_file(self, character_id: str) -> str:
        return os.path.join(self.history_dir, f"{character_id}.txt")

    def get_last_message_time(self, character_id: str) -> Optional[datetime]:
        history_file = self._get_character_history_file(character_id)
        if not os.path.exists(history_file):
            return None
        with open(history_file, 'r') as f:
            lines = f.readlines()
            if not lines:
                return None
            last_line = lines[-1].strip()
            if not last_line:
                return None
            try:
                return datetime.fromisoformat(last_line)
            except ValueError:
                return None

    def format_time_elapsed(self, last_time: Optional[datetime], current_time: datetime) -> str:
        if last_time is None:
            return ""
        delta = current_time - last_time
        seconds = delta.total_seconds()

        if seconds < 60:
            return "a few seconds ago"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif seconds < 86400:
            hours = int(seconds // 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        else:
            days = int(seconds // 86400)
            return f"{days} day{'s' if days != 1 else ''} ago"

    def get_time_elapsed_prefix(self, character_id: str) -> str:
        current_time = datetime.now()
        last_time = self.get_last_message_time(character_id)
        formatted_time = self.format_time_elapsed(last_time, current_time)

        if not formatted_time:
            return ""
        return f"[Last message: {formatted_time}] "
