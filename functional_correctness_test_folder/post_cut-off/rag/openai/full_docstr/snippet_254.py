
import os
import json
from datetime import datetime, timedelta
from typing import Optional


class TimeTracker:
    '''时间跟踪器'''

    def __init__(self, history_dir: str):
        '''
        初始化时间跟踪器
        Args:
            history_dir: 历史记录存储目录
        '''
        self.history_dir = history_dir
        os.makedirs(self.history_dir, exist_ok=True)

    def _get_character_history_file(self, character_id: str) -> str:
        '''
        获取角色历史记录文件路径
        Args:
            character_id: 角色ID
        Returns:
            历史记录文件路径
        '''
        return os.path.join(self.history_dir, f'{character_id}.json')

    def get_last_message_time(self, character_id: str) -> Optional[datetime]:
        '''
        获取角色最后一条消息的时间
        Args:
            character_id: 角色ID
        Returns:
            最后一条消息的时间，如果没有历史记录则返回None
        '''
        file_path = self._get_character_history_file(character_id)
        if not os.path.exists(file_path):
            return None

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            return None

        if not isinstance(data, list) or not data:
            return None

        # Assume each entry has a 'time' field in ISO format
        last_entry = data[-1]
        time_str = last_entry.get('time')
        if not time_str:
            return None

        try:
            return datetime.fromisoformat(time_str)
        except ValueError:
            return None

    def format_time_elapsed(self, last_time: Optional[datetime], current_time: datetime) -> str:
        '''
        格式化时间间隔
        Args:
            last_time: 上次时间
            current_time: 当前时间
        Returns:
            格式化的时间间隔字符串
        '''
        if last_time is None:
            return '无记录'

        delta: timedelta = current_time - last_time
        total_seconds = int(delta.total_seconds())

        days = total_seconds // 86400
        if days > 0:
            return f'{days}天'

        hours = (total_seconds % 86400) // 3600
        if hours > 0:
            return f'{hours}小时'

        minutes = (total_seconds % 3600) // 60
        if minutes > 0:
            return f'{minutes}分钟'

        seconds = total_seconds % 60
        return f'{seconds}秒'

    def get_time_elapsed_prefix(self, character_id: str) -> str:
        '''
        获取时间间隔前缀
        Args:
            character_id: 角色ID
        Returns:
            时间间隔前缀，如"距上次对话xx"
        '''
        last_time = self.get_last_message_time(character_id)
        now = datetime.now()
        elapsed = self.format_time_elapsed(last_time, now)
        return f'距上次对话{elapsed}'
