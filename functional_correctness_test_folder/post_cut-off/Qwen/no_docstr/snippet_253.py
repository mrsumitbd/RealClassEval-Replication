
from typing import List, Dict
import json


class PromptLogger:

    def __init__(self, log_file: str = 'log.txt'):
        self.log_file = log_file
        self.logs = []
        self._load_logs()

    def log_prompt(self, messages: List[Dict[str, str]], character_name: str = None, user_query: str = None):
        log_entry = {
            'messages': messages,
            'character_name': character_name,
            'user_query': user_query
        }
        self.logs.append(log_entry)
        self._save_logs()

    def log_formatted_prompt(self, system_prompt: str, user_prompt: str, memory_context: str = '', character_name: str = None, user_query: str = None):
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'memory', 'content': memory_context},
            {'role': 'user', 'content': user_prompt}
        ]
        self.log_prompt(messages, character_name, user_query)

    def get_recent_logs(self, count: int = 10) -> List[Dict]:
        return self.logs[-count:]

    def clear_logs(self):
        self.logs = []
        self._save_logs()

    def _load_logs(self):
        try:
            with open(self.log_file, 'r') as file:
                self.logs = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.logs = []

    def _save_logs(self):
        with open(self.log_file, 'w') as file:
            json.dump(self.logs, file, indent=4)
