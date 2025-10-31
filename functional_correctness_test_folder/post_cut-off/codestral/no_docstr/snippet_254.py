
import os
import json
from datetime import datetime
from typing import Optional


class TimeTracker:

    def __init__(self, history_dir: str):
        self.history_dir = history_dir

    def _get_character_history_file(self, character_id: str) -> str:
        return os.path.join(self.history_dir, f"{character_id}.json")

    def get_last_message_time(self, character_id: str) -> Optional[datetime]:
        history_file = self._get_character_history_file(character_id)
        if not os.path.exists(history_file):
            return None

        with open(history_file, 'r') as f:
            history = json.load(f)

        if not history:
            return None

        last_message = history[-1]
        return datetime.fromisoformat(last_message['time'])

    def format_time_elapsed(self, last_time: Optional[datetime], current_time: datetime) -> str:
        if last_time is None:
            return "No previous messages."

        time_elapsed = current_time - last_time
        days = time_elapsed.days
        hours, remainder = divmod(time_elapsed.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        parts = []
        if days > 0:
            parts.append(f"{days} day{'s' if days != 1 else ''}")
        if hours > 0:
            parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
        if minutes > 0:
            parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")

        if not parts:
            return "Less than a minute ago."

        return f"{', '.join(parts[:-1])} and {parts[-1]} ago" if len(parts) > 1 else f"{parts[0]} ago"

    def get_time_elapsed_prefix(self, character_id: str) -> str:
        last_time = self.get_last_message_time(character_id)
        current_time = datetime.now()
        return self.format_time_elapsed(last_time, current_time)
