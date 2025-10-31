
import json
from typing import List, Dict


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
            'type': 'full_prompt',
            'messages': messages,
            'character_name': character_name,
            'user_query': user_query
        }
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

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
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

    def get_recent_logs(self, count: int = 10) -> List[Dict]:
        '''
        获取最近的日志条目
        参数:
            count: 返回的条目数量
        返回:
            最近的日志条目列表
        '''
        logs = []
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines[-count:]:
                    logs.append(json.loads(line))
        except FileNotFoundError:
            pass
        return logs

    def clear_logs(self):
        '''清空日志文件'''
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write('')
