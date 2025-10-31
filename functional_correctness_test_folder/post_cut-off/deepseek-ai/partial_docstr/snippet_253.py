
from typing import List, Dict
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
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def log_prompt(self, messages: List[Dict[str, str]], character_name: str = None, user_query: str = None):
        '''
        记录完整的提示词到日志文件
        参数:
            messages: 发送给模型的消息列表
            character_name: 角色名称
            user_query: 用户查询（原始请求）
        '''
        log_entry = {
            'type': 'full_prompt',
            'messages': messages,
            'character_name': character_name,
            'user_query': user_query,
            'timestamp': self._get_timestamp()
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
            'user_query': user_query,
            'timestamp': self._get_timestamp()
        }
        self._append_log(log_entry)

    def get_recent_logs(self, count: int = 10) -> List[Dict]:
        '''
        获取最近的日志记录
        参数:
            count: 要获取的日志数量
        返回:
            日志记录列表
        '''
        with open(self.log_file, 'r', encoding='utf-8') as f:
            logs = json.load(f)
        return logs[-count:]

    def clear_logs(self):
        '''
        清空日志文件
        '''
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump([], f)

    def _append_log(self, log_entry: Dict):
        '''
        内部方法：追加日志到文件
        参数:
            log_entry: 日志条目
        '''
        with open(self.log_file, 'r+', encoding='utf-8') as f:
            logs = json.load(f)
            logs.append(log_entry)
            f.seek(0)
            json.dump(logs, f, ensure_ascii=False, indent=2)

    def _get_timestamp(self) -> str:
        '''
        内部方法：获取当前时间戳
        返回:
            时间戳字符串
        '''
        from datetime import datetime
        return datetime.now().isoformat()
