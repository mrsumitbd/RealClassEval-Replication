
from datetime import datetime, timedelta
from typing import Optional
import os
import json


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
            return "No previous message time recorded."
        time_elapsed = current_time - last_time
        return str(time_elapsed)

    def get_time_elapsed_prefix(self, character_id: str) -> str:
        last_time = self.get_last_message_time(character_id)
        current_time = datetime.now()
        time_elapsed = self.format_time_elapsed(last_time, current_time)
        return f"Time since last message: {time_elapsed}"
