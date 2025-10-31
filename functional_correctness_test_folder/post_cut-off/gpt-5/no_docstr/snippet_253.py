from typing import List, Dict, Optional
import json
import os
from datetime import datetime


class PromptLogger:

    def __init__(self, log_file: str = 'log.txt'):
        self.log_file = log_file
        os.makedirs(os.path.dirname(self.log_file) or ".", exist_ok=True)
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8') as f:
                pass

    def log_prompt(self, messages: List[Dict[str, str]], character_name: str = None, user_query: str = None):
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "type": "messages",
            "character_name": character_name,
            "user_query": user_query,
            "messages": messages,
        }
        self._write_entry(entry)

    def log_formatted_prompt(self, system_prompt: str, user_prompt: str, memory_context: str = '', character_name: str = None, user_query: str = None):
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "type": "formatted",
            "character_name": character_name,
            "user_query": user_query,
            "system_prompt": system_prompt,
            "memory_context": memory_context,
            "user_prompt": user_prompt,
        }
        self._write_entry(entry)

    def get_recent_logs(self, count: int = 10) -> List[Dict]:
        if not os.path.exists(self.log_file):
            return []
        lines = []
        with open(self.log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        recent = []
        # small optimization for large files
        for line in reversed(lines[-count * 2:]):
            line = line.strip()
            if not line:
                continue
            try:
                recent.append(json.loads(line))
                if len(recent) >= count:
                    break
            except json.JSONDecodeError:
                continue
        return list(reversed(recent))

    def clear_logs(self):
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.truncate(0)

    def _write_entry(self, entry: Dict):
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
