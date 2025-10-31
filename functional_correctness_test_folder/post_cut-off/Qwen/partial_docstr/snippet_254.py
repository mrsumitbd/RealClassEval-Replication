
import os
import json
from datetime import datetime
from typing import Optional


class TimeTracker:

    def __init__(self, history_dir: str):
        self.history_dir = history_dir
        if not os.path.exists(self.history_dir):
            os.makedirs(self.history_dir)

    def _get_character_history_file(self, character_id: str) -> str:
        return os.path.join(self.history_dir, f"{character_id}_history.json")

    def get_last_message_time(self, character_id: str) -> Optional[datetime]:
        history_file = self._get_character_history_file(character_id)
        if os.path.exists(history_file):
            with open(history_file, 'r') as file:
                data = json.load(file)
                last_time_str = data.get('last_message_time')
                if last_time_str:
                    return datetime.fromisoformat(last_time_str)
        return None

    def format_time_elapsed(self, last_time: Optional[datetime], current_time: datetime) -> str:
        if last_time is None:
            return "无历史记录"
        time_elapsed = current_time - last_time
        days = time_elapsed.days
        seconds = time_elapsed.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        if days > 0:
            return f"{days}天{hours}小时{minutes}分钟"
        elif hours > 0:
            return f"{hours}小时{minutes}分钟"
        elif minutes > 0:
            return f"{minutes}分钟"
        else:
            return "几秒钟"

    def get_time_elapsed_prefix(self, character_id: str) -> str:
        current_time = datetime.now()
        last_time = self.get_last_message_time(character_id)
        time_elapsed_str = self.format_time_elapsed(last_time, current_time)
        return f"距上次对话{time_elapsed_str}"
