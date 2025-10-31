from __future__ import annotations

import os
from datetime import datetime, timedelta
from typing import Optional


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
        safe_id = str(character_id).strip().replace(os.sep, "_")
        return os.path.join(self.history_dir, safe_id)

    def get_last_message_time(self, character_id: str) -> Optional[datetime]:
        path = self._get_character_history_file(character_id)
        if not os.path.exists(path):
            return None
        try:
            mtime = os.path.getmtime(path)
            return datetime.fromtimestamp(mtime)
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
        if last_time > current_time:
            return "刚刚"

        delta: timedelta = current_time - last_time
        seconds = int(delta.total_seconds())
        if seconds < 5:
            return "刚刚"

        units = [
            ("年", 365 * 24 * 3600),
            ("月", 30 * 24 * 3600),
            ("天", 24 * 3600),
            ("小时", 3600),
            ("分钟", 60),
            ("秒", 1),
        ]

        parts = []
        remainder = seconds
        for name, size in units:
            if remainder >= size:
                qty = remainder // size
                remainder = remainder % size
                parts.append(f"{qty}{name}")
            if len(parts) >= 2:
                break

        return "".join(parts) if parts else "刚刚"

    def get_time_elapsed_prefix(self, character_id: str) -> str:
        '''
        获取时间间隔前缀
        Args:
            character_id: 角色ID
        Returns:
            时间间隔前缀，如"距上次对话xx"
        '''
        last = self.get_last_message_time(character_id)
        now = datetime.now()
        formatted = self.format_time_elapsed(last, now)
        if formatted == "首次对话":
            return formatted
        return f"距上次对话{formatted}"
