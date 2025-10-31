from typing import List, Dict, Optional
import json
import os
from datetime import datetime
import threading


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
        # 确保日志文件存在
        try:
            os.makedirs(os.path.dirname(self.log_file), exist_ok=True) if os.path.dirname(
                self.log_file) else None
            if not os.path.exists(self.log_file):
                with open(self.log_file, 'w', encoding='utf-8') as f:
                    pass
        except Exception:
            pass

    def log_prompt(self, messages: List[Dict[str, str]], character_name: str = None, user_query: str = None):
        '''
        记录完整的提示词到日志文件
        参数:
            messages: 发送给模型的消息列表
            character_name: 角色名称
            user_query: 用户查询（原始请求）
        '''
        entry = {
            'timestamp': datetime.now().iso8601() if hasattr(datetime.now(), 'iso8601') else datetime.now().isoformat(),
            'type': 'raw',
            'character_name': character_name,
            'user_query': user_query,
            'messages': messages,
        }
        data = json.dumps(entry, ensure_ascii=False)
        with self._lock:
            try:
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write(data + '\n')
            except Exception:
                pass

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
            'timestamp': datetime.now().iso8601() if hasattr(datetime.now(), 'iso8601') else datetime.now().isoformat(),
            'type': 'formatted',
            'character_name': character_name,
            'user_query': user_query,
            'system_prompt': system_prompt,
            'user_prompt': user_prompt,
            'memory_context': memory_context or '',
        }
        data = json.dumps(entry, ensure_ascii=False)
        with self._lock:
            try:
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write(data + '\n')
            except Exception:
                pass

    def get_recent_logs(self, count: int = 10) -> List[Dict]:
        with self._lock:
            try:
                if not os.path.exists(self.log_file):
                    return []
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                recent = lines[-count:] if count > 0 else []
                result: List[Dict] = []
                for line in recent:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        result.append(json.loads(line))
                    except Exception:
                        continue
                return result
            except Exception:
                return []

    def clear_logs(self):
        with self._lock:
            try:
                with open(self.log_file, 'w', encoding='utf-8'):
                    pass
            except Exception:
                pass
