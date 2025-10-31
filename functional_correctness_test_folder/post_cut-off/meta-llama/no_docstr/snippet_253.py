
from typing import List, Dict


class PromptLogger:

    def __init__(self, log_file: str = 'log.txt'):
        self.log_file = log_file
        try:
            with open(self.log_file, 'r'):
                pass
        except FileNotFoundError:
            with open(self.log_file, 'w') as f:
                f.write('[]')

    def log_prompt(self, messages: List[Dict[str, str]], character_name: str = None, user_query: str = None):
        import json
        with open(self.log_file, 'r+') as f:
            logs = json.load(f)
            log_entry = {
                'messages': messages,
                'character_name': character_name,
                'user_query': user_query
            }
            logs.append(log_entry)
            f.seek(0)
            json.dump(logs, f)
            f.truncate()

    def log_formatted_prompt(self, system_prompt: str, user_prompt: str, memory_context: str = '', character_name: str = None, user_query: str = None):
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'context', 'content': memory_context},
            {'role': 'user', 'content': user_prompt}
        ]
        self.log_prompt(messages, character_name, user_query)

    def get_recent_logs(self, count: int = 10) -> List[Dict]:
        import json
        with open(self.log_file, 'r') as f:
            logs = json.load(f)
            return logs[-count:]

    def clear_logs(self):
        with open(self.log_file, 'w') as f:
            f.write('[]')
