
from typing import List, Dict
import json
import os
import threading
from datetime import datetime


class PromptLogger:

    def __init__(self, log_file: str = 'log.txt'):
        self.log_file = log_file
        self._lock = threading.Lock()
        # Ensure the log file exists
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8') as f:
                pass

    def log_prompt(self, messages: List[Dict[str, str]], character_name: str = None, user_query: str = None):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'type': 'prompt',
            'messages': messages,
            'character_name': character_name,
            'user_query': user_query
        }
        with self._lock:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

    def log_formatted_prompt(self, system_prompt: str, user_prompt: str, memory_context: str = '', character_name: str = None, user_query: str = None):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'type': 'formatted_prompt',
            'system_prompt': system_prompt,
            'user_prompt': user_prompt,
            'memory_context': memory_context,
            'character_name': character_name,
            'user_query': user_query
        }
        with self._lock:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

    def get_recent_logs(self, count: int = 10) -> List[Dict]:
        logs = []
        with self._lock:
            if not os.path.exists(self.log_file):
                return []
            with open(self.log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines[-count:]:
                    line = line.strip()
                    if line:
                        try:
                            logs.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
        return logs

    def clear_logs(self):
        with self._lock:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                pass
