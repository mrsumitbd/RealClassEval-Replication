from typing import List, Dict, Optional
from datetime import datetime
from collections import deque
import threading
import json
import os


class PromptLogger:
    '''提示词日志记录器'''

    def __init__(self, log_file: str = 'log.txt'):
        '''
        初始化日志记录器
        参数:
            log_file: 日志文件路径
        '''
        self.log_file = log_file
        self._lock = threading.Lock()
        dir_name = os.path.dirname(os.path.abspath(self.log_file))
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8'):
                pass

    def _now(self) -> str:
        return datetime.utcnow().isoformat(timespec='seconds') + 'Z'

    def _append_record(self, record: Dict):
        line = json.dumps(record, ensure_ascii=False)
        with self._lock:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(line + '\n')

    def log_prompt(self, messages: List[Dict[str, str]], character_name: str = None, user_query: str = None):
        '''
        记录完整的提示词到日志文件
        参数:
            messages: 发送给模型的消息列表
            character_name: 角色名称
            user_query: 用户查询（原始请求）
        '''
        record = {
            'timestamp': self._now(),
            'type': 'full_prompt',
            'character_name': character_name,
            'user_query': user_query,
            'messages': messages,
        }
        self._append_record(record)

    def log_formatted_prompt(self, system_prompt: str, user_prompt: str, memory_context: str = '', character_name: str = None, user_query: str = None):
        '''
        记录格式化的提示词（分别记录system和user部分）
        参数:
            system_prompt: 系统提示词
            user_prompt: 用户提示词
            memory_context: 记忆上下文
            character_name: 角色名称
            user_query: 原始用户查询（未经任何加工的用户输入）
        '''
        record = {
            'timestamp': self._now(),
            'type': 'formatted_prompt',
            'character_name': character_name,
            'user_query': user_query,
            'system_prompt': system_prompt,
            'user_prompt': user_prompt,
            'memory_context': memory_context,
        }
        self._append_record(record)

    def get_recent_logs(self, count: int = 10) -> List[Dict]:
        '''
        获取最近的日志条目
        参数:
            count: 返回的条目数量
        返回:
            最近的日志条目列表
        '''
        items = deque(maxlen=max(1, count))
        with self._lock:
            if not os.path.exists(self.log_file):
                return []
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        items.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        return list(items)

    def clear_logs(self):
        '''清空日志文件'''
        with self._lock:
            with open(self.log_file, 'w', encoding='utf-8'):
                pass
