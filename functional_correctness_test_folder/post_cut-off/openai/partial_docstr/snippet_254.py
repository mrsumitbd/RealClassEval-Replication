
import os
import json
from datetime import datetime, timedelta
from typing import Optional


class TimeTracker:
    def __init__(self, history_dir: str):
        """
        初始化时间跟踪器
        Args:
            history_dir: 历史记录存储目录
        """
        self.history_dir = history_dir
        os.makedirs(self.history_dir, exist_ok=True)

    def _get_character_history_file(self, character_id: str) -> str:
        """
        获取角色历史记录文件路径
        Args:
            character_id: 角色ID
        Returns:
            历史记录文件路径
        """
        return os.path.join(self.history_dir, f"{character_id}.json")

    def get_last_message_time(self, character_id: str) -> Optional[datetime]:
        """
        读取角色历史文件，返回上次消息时间
        """
        file_path = self._get_character_history_file(character_id)
        if not os.path.exists(file_path):
            return None
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            ts = data.get("last_message_time")
            if ts:
                return datetime.fromisoformat(ts)
        except Exception:
            pass
        return None

    def format_time_elapsed(self, last_time: Optional[datetime], current_time: datetime) -> str:
        """
        格式化时间间隔
        Args:
            last_time: 上次时间
            current_time: 当前时间
        Returns:
            格式化的时间间隔字符串
        """
        if last_time is None:
            return "未知"
        delta: timedelta = current_time - last_time
        days = delta.days
        seconds = delta.seconds
        parts = []
        if days:
            parts.append(f"{days}天")
        if seconds >= 3600:
            hours = seconds // 3600
            parts.append(f"{hours}小时")
            seconds %= 3600
        if seconds >= 60:
            minutes = seconds // 60
            parts.append(f"{minutes}分钟")
            seconds %= 60
        if seconds > 0 or not parts:
            parts.append(f"{seconds}秒")
        return "".join(parts)

    def get_time_elapsed_prefix(self, character_id: str) -> str:
        """
        获取时间间隔前缀
        Args:
            character_id: 角色ID
        Returns:
            时间间隔前缀，如"距上次对话xx"
        """
        last_time = self.get_last_message_time(character_id)
        current_time = datetime.now()
        elapsed = self.format_time_elapsed(last_time, current_time)
        if elapsed == "未知":
            return ""
        return f"距上次对话{elapsed}"
