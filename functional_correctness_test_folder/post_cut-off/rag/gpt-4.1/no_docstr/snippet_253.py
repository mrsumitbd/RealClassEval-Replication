import os
import json
from typing import List, Dict, Optional


class PromptLogger:
    '''提示词日志记录器'''

    def __init__(self, log_file: str = 'log.txt'):
        '''
        初始化日志记录器
        参数:
            log_file: 日志文件路径
        '''
        self.log_file = log_file

    def log_prompt(self, messages: List[Dict[str, str]], character_name: str = None, user_query: str = None):
        '''
        记录完整的提示词到日志文件
        参数:
            messages: 发送给模型的消息列表
            character_name: 角色名称
            user_query: 用户查询（原始请求）
        '''
        log_entry = {
            'type': 'prompt',
            'messages': messages,
            'character_name': character_name,
            'user_query': user_query
        }
        self._append_log(log_entry)

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
        log_entry = {
            'type': 'formatted_prompt',
            'system_prompt': system_prompt,
            'user_prompt': user_prompt,
            'memory_context': memory_context,
            'character_name': character_name,
            'user_query': user_query
        }
        self._append_log(log_entry)

    def get_recent_logs(self, count: int = 10) -> List[Dict]:
        '''
        获取最近的日志条目
        参数:
            count: 返回的条目数量
        返回:
            最近的日志条目列表
        '''
        if not os.path.exists(self.log_file):
            return []
        logs = []
        with open(self.log_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    logs.append(json.loads(line))
                except Exception:
                    continue
        return logs[-count:] if count > 0 else logs

    def clear_logs(self):
        '''清空日志文件'''
        open(self.log_file, 'w', encoding='utf-8').close()

    def _append_log(self, log_entry: Dict):
        log_entry['timestamp'] = self._get_timestamp()
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

    def _get_timestamp(self):
        import datetime
        return datetime.datetime.now().isoformat()
