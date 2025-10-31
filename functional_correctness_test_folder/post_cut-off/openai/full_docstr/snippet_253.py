
import json
import os
import datetime
from pathlib import Path
from typing import List, Dict, Optional


class PromptLogger:
    '''提示词日志记录器'''

    def __init__(self, log_file: str = 'log.txt'):
        '''
        初始化日志记录器
        参数:
            log_file: 日志文件路径
        '''
        self.log_path = Path(log_file)
        # 确保日志文件存在
        if not self.log_path.exists():
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
            self.log_path.touch()

    def _write_entry(self, entry: Dict):
        with self.log_path.open('a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    def log_prompt(self, messages: List[Dict[str, str]], character_name: Optional[str] = None,
                   user_query: Optional[str] = None):
        '''
        记录完整的提示词到日志文件
        参数:
            messages: 发送给模型的消息列表
            character_name: 角色名称
            user_query: 用户查询（原始请求）
        '''
        entry = {
            'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
            'type': 'full',
            'messages': messages,
            'character_name': character_name,
            'user_query': user_query
        }
        self._write_entry(entry)

    def log_formatted_prompt(self, system_prompt: str, user_prompt: str,
                             memory_context: str = '', character_name: Optional[str] = None,
                             user_query: Optional[str] = None):
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
            'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
            'type': 'formatted',
            'system_prompt': system_prompt,
            'user_prompt': user_prompt,
            'memory_context': memory_context,
            'character_name': character_name,
            'user_query': user_query
        }
        self._write_entry(entry)

    def get_recent_logs(self, count: int = 10) -> List[Dict]:
        '''
        获取最近的日志条目
        参数:
            count: 返回的条目数量
        返回:
            最近的日志条目列表
        '''
        if not self.log_path.exists():
            return []

        with self.log_path.open('r', encoding='utf-8') as f:
            lines = f.readlines()

        recent_lines = lines[-count:] if count > 0 else []
        recent_entries = []
        for line in recent_lines:
            try:
                recent_entries.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue
        return recent_entries

    def clear_logs(self):
        '''清空日志文件'''
        self.log_path.unlink(missing_ok=True)
        self.log_path.touch()
