from typing import List, Dict
import os
import json
import threading
from datetime import datetime, timezone
from uuid import uuid4


class PromptLogger:
    '''提示词日志记录器'''

    def __init__(self, log_file: str = 'log.txt'):
        '''
        初始化日志记录器
        参数:
            log_file: 日志文件路径
        '''
        self.log_file = log_file
        self._lock = threading.RLock()
        log_dir = os.path.dirname(os.path.abspath(self.log_file))
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8'):
                pass

    def _now_iso(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _append_entry(self, entry: Dict):
        entry.setdefault('id', uuid4().hex)
        entry.setdefault('timestamp', self._now_iso())
        with self._lock, open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    def log_prompt(self, messages: List[Dict[str, str]], character_name: str = None, user_query: str = None):
        '''
        记录完整的提示词到日志文件
        参数:
            messages: 发送给模型的消息列表
            character_name: 角色名称
            user_query: 用户查询（原始请求）
        '''
        entry = {
            'type': 'full_prompt',
            'character_name': character_name,
            'user_query': user_query,
            'messages': messages,
        }
        self._append_entry(entry)

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
        entry = {
            'type': 'formatted_prompt',
            'character_name': character_name,
            'user_query': user_query,
            'system_prompt': system_prompt,
            'user_prompt': user_prompt,
            'memory_context': memory_context or '',
        }
        self._append_entry(entry)

    def get_recent_logs(self, count: int = 10) -> List[Dict]:
        '''
        获取最近的日志条目
        参数:
            count: 返回的条目数量
        返回:
            最近的日志条目列表
        '''
        if count <= 0:
            return []
        if not os.path.exists(self.log_file):
            return []
        with self._lock, open(self.log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        result: List[Dict] = []
        for line in reversed(lines):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                result.append(entry)
                if len(result) >= count:
                    break
            except json.JSONDecodeError:
                continue
        return result

    def clear_logs(self):
        '''清空日志文件'''
        with self._lock, open(self.log_file, 'w', encoding='utf-8'):
            pass
