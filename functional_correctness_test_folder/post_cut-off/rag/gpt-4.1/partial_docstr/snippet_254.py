import os
import json
from datetime import datetime
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
        if not os.path.exists(self.history_dir):
            os.makedirs(self.history_dir, exist_ok=True)

    def _get_character_history_file(self, character_id: str) -> str:
        '''
        获取角色历史记录文件路径
        Args:
            character_id: 角色ID
        Returns:
            历史记录文件路径
        '''
        filename = f"{character_id}.json"
        return os.path.join(self.history_dir, filename)

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
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list) or not data:
                return None
            last_msg = data[-1]
            # 假设消息有'time'字段，格式为ISO 8601字符串
            time_str = last_msg.get("time")
            if not time_str:
                return None
            return datetime.fromisoformat(time_str)
        except Exception:
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
            return "首次对话"
        delta = current_time - last_time
        seconds = int(delta.total_seconds())
        if seconds < 60:
            return f"{seconds}秒"
        minutes = seconds // 60
        if minutes < 60:
            return f"{minutes}分钟"
        hours = minutes // 60
        if hours < 24:
            return f"{hours}小时"
        days = hours // 24
        if days < 30:
            return f"{days}天"
        months = days // 30
        if months < 12:
            return f"{months}个月"
        years = months // 12
        return f"{years}年"

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
        elapsed_str = self.format_time_elapsed(last_time, now)
        if elapsed_str == "首次对话":
            return elapsed_str
        return f"距上次对话{elapsed_str}"
