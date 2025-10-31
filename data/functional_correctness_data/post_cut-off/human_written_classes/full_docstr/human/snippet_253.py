from datetime import datetime
import json
import os
from typing import List, Dict, Any
import logging

class PromptLogger:
    """提示词日志记录器"""

    def __init__(self, log_file: str='log.txt'):
        """
        初始化日志记录器

        参数:
            log_file: 日志文件路径
        """
        self.log_file = log_file
        self.logger = logging.getLogger('PromptLogger')
        log_dir = os.path.dirname(log_file) if os.path.dirname(log_file) else '.'
        os.makedirs(log_dir, exist_ok=True)

    def log_prompt(self, messages: List[Dict[str, str]], character_name: str=None, user_query: str=None):
        """
        记录完整的提示词到日志文件

        参数:
            messages: 发送给模型的消息列表
            character_name: 角色名称
            user_query: 用户查询（原始请求）
        """
        try:
            log_entry = {'timestamp': datetime.now().isoformat(), 'character_name': character_name, 'original_user_request': user_query, 'user_query': user_query, 'messages': messages, 'total_messages': len(messages)}
            total_chars = sum((len(msg.get('content', '')) for msg in messages))
            log_entry['total_characters'] = total_chars
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write('=' * 80 + '\n')
                character_info = f' - 角色: {character_name}' if character_name else ''
                f.write(f'[{datetime.now().isoformat()}] 发送给AI的完整请求记录{character_info}\n')
                f.write('=' * 80 + '\n')
                if user_query:
                    f.write('🔥【原始用户请求 - 未经任何加工】🔥:\n')
                    f.write(f'>>> {user_query}\n')
                    f.write('-' * 50 + '\n')
                f.write('【发送给AI的完整消息】:\n')
                f.write(json.dumps(log_entry, ensure_ascii=False, indent=2) + '\n')
                f.write('=' * 80 + '\n\n')
            self.logger.info(f'记录提示词日志: {len(messages)} 条消息, {total_chars} 字符')
        except Exception as e:
            self.logger.error(f'记录提示词日志失败: {e}')

    def log_formatted_prompt(self, system_prompt: str, user_prompt: str, memory_context: str='', character_name: str=None, user_query: str=None):
        """
        记录格式化的提示词（分别记录system和user部分）

        参数:
            system_prompt: 系统提示词
            user_prompt: 用户提示词
            memory_context: 记忆上下文
            character_name: 角色名称
            user_query: 原始用户查询（未经任何加工的用户输入）
        """
        try:
            messages = []
            if system_prompt:
                messages.append({'role': 'system', 'content': system_prompt})
            user_content = ''
            if memory_context:
                user_content += memory_context + '\n\n'
            user_content += user_prompt
            messages.append({'role': 'user', 'content': user_content})
            self.log_prompt(messages, character_name, user_query)
        except Exception as e:
            self.logger.error(f'记录格式化提示词失败: {e}')

    def get_recent_logs(self, count: int=10) -> List[Dict]:
        """
        获取最近的日志条目

        参数:
            count: 返回的条目数量

        返回:
            最近的日志条目列表
        """
        try:
            if not os.path.exists(self.log_file):
                return []
            logs = []
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        log_entry = json.loads(line.strip())
                        logs.append(log_entry)
                    except json.JSONDecodeError:
                        continue
            return logs[-count:] if len(logs) > count else logs
        except Exception as e:
            self.logger.error(f'读取日志失败: {e}')
            return []

    def clear_logs(self):
        """清空日志文件"""
        try:
            if os.path.exists(self.log_file):
                os.remove(self.log_file)
            self.logger.info('日志文件已清空')
        except Exception as e:
            self.logger.error(f'清空日志失败: {e}')