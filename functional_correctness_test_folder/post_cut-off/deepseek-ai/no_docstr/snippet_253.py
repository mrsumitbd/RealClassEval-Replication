
from typing import List, Dict
import json
import os


class PromptLogger:

    def __init__(self, log_file: str = 'log.txt'):
        self.log_file = log_file
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                json.dump([], f)

    def log_prompt(self, messages: List[Dict[str, str]], character_name: str = None, user_query: str = None):
        log_entry = {
            'messages': messages,
            'character_name': character_name,
            'user_query': user_query
        }
        self._append_log(log_entry)

    def log_formatted_prompt(self, system_prompt: str, user_prompt: str, memory_context: str = '', character_name: str = None, user_query: str = None):
        log_entry = {
            'system_prompt': system_prompt,
            'user_prompt': user_prompt,
            'memory_context': memory_context,
            'character_name': character_name,
            'user_query': user_query
        }
        self._append_log(log_entry)

    def get_recent_logs(self, count: int = 10) -> List[Dict]:
        with open(self.log_file, 'r') as f:
            logs = json.load(f)
        return logs[-count:]

    def clear_logs(self):
        with open(self.log_file, 'w') as f:
            json.dump([], f)

    def _append_log(self, log_entry: Dict):
        with open(self.log_file, 'r+') as f:
            logs = json.load(f)
            logs.append(log_entry)
            f.seek(0)
            json.dump(logs, f)
