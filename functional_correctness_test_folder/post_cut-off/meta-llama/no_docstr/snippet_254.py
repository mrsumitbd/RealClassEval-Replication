
import os
from datetime import datetime
from typing import Optional


class TimeTracker:

    def __init__(self, history_dir: str):
        self.history_dir = history_dir

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
            try:
                return datetime.strptime(last_line, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return None

    def format_time_elapsed(self, last_time: Optional[datetime], current_time: datetime) -> str:
        if last_time is None:
            return "N/A"
        time_diff = current_time - last_time
        days = time_diff.days
        hours, remainder = divmod(time_diff.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        if days > 0:
            return f"{days} days, {hours} hours, {minutes} minutes ago"
        elif hours > 0:
            return f"{hours} hours, {minutes} minutes ago"
        else:
            return f"{minutes} minutes ago"

    def get_time_elapsed_prefix(self, character_id: str) -> str:
        last_time = self.get_last_message_time(character_id)
        current_time = datetime.now()
        return self.format_time_elapsed(last_time, current_time)
