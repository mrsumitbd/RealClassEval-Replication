
import os
import json
from datetime import datetime
from typing import Optional


class TimeTracker:

    def __init__(self, history_dir: str):
        self.history_dir = history_dir
        os.makedirs(history_dir, exist_ok=True)

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
            return "这是我们第一次对话"
        delta = current_time - last_time
        days = delta.days
        seconds = delta.seconds
        hours, remainder = divmod(seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        if days > 0:
            return f"距上次对话{days}天{hours}小时"
        elif hours > 0:
            return f"距上次对话{hours}小时{minutes}分钟"
        else:
            return f"距上次对话{minutes}分钟"

    def get_time_elapsed_prefix(self, character_id: str) -> str:
        last_time = self.get_last_message_time(character_id)
        current_time = datetime.now()
        return self.format_time_elapsed(last_time, current_time)
