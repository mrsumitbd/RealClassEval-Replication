
import os
from typing import Optional
from datetime import datetime, timedelta


class TimeTracker:

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
        safe_id = character_id.replace('/', '_').replace('\\', '_')
        return os.path.join(self.history_dir, f"{safe_id}.txt")

    def get_last_message_time(self, character_id: str) -> Optional[datetime]:
        file_path = self._get_character_history_file(character_id)
        if not os.path.exists(file_path):
            return None
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if not lines:
                    return None
                last_line = lines[-1].strip()
                if not last_line:
                    return None
                # Assume the last line is an ISO datetime string
                return datetime.fromisoformat(last_line)
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
        days = delta.days
        seconds = delta.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        if days > 0:
            return f"{days}天{hours}小时"
        elif hours > 0:
            return f"{hours}小时{minutes}分钟"
        elif minutes > 0:
            return f"{minutes}分钟"
        else:
            return "刚刚"

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
