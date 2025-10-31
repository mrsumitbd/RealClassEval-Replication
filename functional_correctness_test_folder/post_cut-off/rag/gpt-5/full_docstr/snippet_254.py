from __future__ import annotations

import json
import os
from datetime import datetime, timezone
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
        safe_id = str(character_id).strip().replace(os.sep, "_")
        return os.path.join(self.history_dir, f"{safe_id}.log")

    def get_last_message_time(self, character_id: str) -> Optional[datetime]:
        '''
        获取角色最后一条消息的时间
        Args:
            character_id: 角色ID
        Returns:
            最后一条消息的时间，如果没有历史记录则返回None
        '''
        path = self._get_character_history_file(character_id)
        if not os.path.exists(path):
            return None

        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception:
            return None

        # 从最后一行开始向上查找可解析的时间
        for raw_line in reversed(lines):
            line = raw_line.strip()
            if not line:
                continue
            dt = self._parse_time_from_line(line)
            if dt is not None:
                return dt
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

        lt, ct = self._normalize_datetimes(last_time, current_time)
        delta = ct - lt
        total_seconds = int(delta.total_seconds())
        if total_seconds <= 0:
            return "不到1分钟"

        minutes = total_seconds // 60
        hours = minutes // 60
        days = hours // 24

        if days > 0:
            rem_hours = hours % 24
            rem_minutes = minutes % 60
            parts = []
            parts.append(f"{days}天")
            if rem_hours > 0:
                parts.append(f"{rem_hours}小时")
            if rem_minutes > 0:
                parts.append(f"{rem_minutes}分钟")
            return "".join(parts)

        if hours > 0:
            rem_minutes = minutes % 60
            if rem_minutes > 0:
                return f"{hours}小时{rem_minutes}分钟"
            return f"{hours}小时"

        if minutes > 0:
            return f"{minutes}分钟"

        return "不到1分钟"

    def get_time_elapsed_prefix(self, character_id: str) -> str:
        '''
        获取时间间隔前缀
        Args:
            character_id: 角色ID
        Returns:
            时间间隔前缀，如"距上次对话xx"
        '''
        last = self.get_last_message_time(character_id)
        now = datetime.now(timezone.utc)
        text = self.format_time_elapsed(last, now)
        if text == "首次对话":
            return text
        return f"距上次对话{text}"

    # -------------------- internal helpers --------------------

    def _parse_time_from_line(self, line: str) -> Optional[datetime]:
        # JSON line with timestamp fields
        if (line.startswith("{") and line.endswith("}")) or (line.startswith("[") and line.endswith("]")):
            try:
                obj = json.loads(line)
                # Try top-level keys
                for key in ("time", "timestamp", "created_at", "datetime"):
                    if isinstance(obj, dict) and key in obj:
                        return self._parse_timestamp_value(obj[key])
                # If it's a list, try last element as dict
                if isinstance(obj, list) and obj:
                    last = obj[-1]
                    if isinstance(last, dict):
                        for key in ("time", "timestamp", "created_at", "datetime"):
                            if key in last:
                                return self._parse_timestamp_value(last[key])
            except Exception:
                # fall through to other parsing attempts
                pass

        # Numeric epoch or ISO/date string
        return self._parse_timestamp_value(line)

    def _parse_timestamp_value(self, value) -> Optional[datetime]:
        # If it's already a datetime
        if isinstance(value, datetime):
            return value

        # Numeric epoch seconds/milliseconds
        try:
            if isinstance(value, (int, float)) or (isinstance(value, str) and value.strip().replace(".", "", 1).isdigit()):
                num = float(value)
                # treat > 1e12 as milliseconds
                if num > 1e12:
                    num = num / 1000.0
                return datetime.fromtimestamp(num, tz=timezone.utc)
        except Exception:
            pass

        # String datetime formats
        if isinstance(value, str):
            s = value.strip()
            # ISO 8601 handling including trailing Z
            iso = s.replace("Z", "+00:00") if s.endswith("Z") else s
            try:
                return datetime.fromisoformat(iso)
            except Exception:
                pass

            # Common datetime formats
            fmts = [
                "%Y-%m-%d %H:%M:%S",
                "%Y/%m/%d %H:%M:%S",
                "%Y-%m-%d %H:%M",
                "%Y/%m/%d %H:%M",
                "%Y-%m-%d",
                "%Y/%m/%d",
            ]
            for fmt in fmts:
                try:
                    # naive datetime assumed local; convert to UTC naive-equivalent by assuming local time.
                    # To avoid timezone ambiguity, we keep it naive and let normalization handle.
                    dt = datetime.strptime(s, fmt)
                    return dt
                except Exception:
                    continue

        return None

    def _normalize_datetimes(self, a: datetime, b: datetime) -> tuple[datetime, datetime]:
        # Align timezone awareness between two datetimes
        a_is_aware = a.tzinfo is not None and a.tzinfo.utcoffset(a) is not None
        b_is_aware = b.tzinfo is not None and b.tzinfo.utcoffset(b) is not None

        if a_is_aware and b_is_aware:
            return a, b

        if a_is_aware and not b_is_aware:
            # Assume naive is in UTC for consistency
            b_aware = b.replace(tzinfo=timezone.utc)
            return a, b_aware

        if not a_is_aware and b_is_aware:
            a_aware = a.replace(tzinfo=timezone.utc)
            return a_aware, b

        # both naive
        return a, b
