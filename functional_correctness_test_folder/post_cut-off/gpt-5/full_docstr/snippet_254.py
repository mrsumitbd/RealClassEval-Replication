from __future__ import annotations

import json
import os
from datetime import datetime, timedelta
from typing import Optional, Any


class TimeTracker:
    '''时间跟踪器'''

    def __init__(self, history_dir: str):
        '''
        初始化时间跟踪器
        Args:
            history_dir: 历史记录存储目录
        '''
        self.history_dir = os.path.abspath(history_dir)
        os.makedirs(self.history_dir, exist_ok=True)
        self._prefer_exts = (".jsonl", ".json", ".txt")

    def _get_character_history_file(self, character_id: str) -> str:
        '''
        获取角色历史记录文件路径
        Args:
            character_id: 角色ID
        Returns:
            历史记录文件路径
        '''
        base = os.path.join(self.history_dir, character_id)
        for ext in self._prefer_exts:
            candidate = base + ext
            if os.path.isfile(candidate):
                return candidate
        # 默认返回 .jsonl 路径（若文件不存在，其他方法将据此判断）
        return base + self._prefer_exts[0]

    def get_last_message_time(self, character_id: str) -> Optional[datetime]:
        '''
        获取角色最后一条消息的时间
        Args:
            character_id: 角色ID
        Returns:
            最后一条消息的时间，如果没有历史记录则返回None
        '''
        path = self._get_character_history_file(character_id)
        if not os.path.isfile(path):
            return None

        _, ext = os.path.splitext(path)
        try:
            if ext == ".jsonl":
                return self._last_time_from_jsonl(path)
            elif ext == ".json":
                return self._last_time_from_json(path)
            elif ext == ".txt":
                return self._last_time_from_txt(path)
            else:
                # 未知扩展名，尝试通用读取
                return self._last_time_from_jsonl(path) or self._last_time_from_json(path) or self._last_time_from_txt(path)
        except Exception:
            # 兜底：尝试使用文件修改时间
            try:
                return datetime.fromtimestamp(os.path.getmtime(path))
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
            return "未知"

        # 统一处理为朴素时间（避免时区混用问题）
        if getattr(last_time, "tzinfo", None) is not None:
            last_time = last_time.replace(tzinfo=None)
        if getattr(current_time, "tzinfo", None) is not None:
            current_time = current_time.replace(tzinfo=None)

        delta = current_time - last_time
        total_seconds = int(delta.total_seconds())
        if total_seconds < 0:
            total_seconds = -total_seconds

        if total_seconds < 5:
            return "刚刚"
        if total_seconds < 60:
            return f"{total_seconds}秒"

        minutes = total_seconds // 60
        seconds = total_seconds % 60
        if total_seconds < 3600:
            if seconds >= 1:
                return f"{minutes}分钟{seconds}秒"
            return f"{minutes}分钟"

        hours = minutes // 60
        minutes = minutes % 60
        if total_seconds < 86400:
            if minutes >= 1:
                return f"{hours}小时{minutes}分钟"
            return f"{hours}小时"

        days = hours // 24
        hours = hours % 24
        if days < 30:
            if hours >= 1:
                return f"{days}天{hours}小时"
            return f"{days}天"

        months = days // 30
        days = days % 30
        if months < 12:
            if days >= 1:
                return f"{months}个月{days}天"
            return f"{months}个月"

        years = months // 12
        months = months % 12
        if months >= 1:
            return f"{years}年{months}个月"
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
        if last_time is None:
            return "首次对话"
        now = datetime.now()
        return f"距上次对话{self.format_time_elapsed(last_time, now)}"

    # ---------------- 内部工具方法 ----------------

    def _last_time_from_jsonl(self, path: str) -> Optional[datetime]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
            for line in reversed(lines):
                dt = self._extract_time_from_any(line)
                if dt:
                    return dt
        except Exception:
            return None
        return None

    def _last_time_from_json(self, path: str) -> Optional[datetime]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            return None

        # 常见结构 1：列表，每个元素是一条消息
        if isinstance(data, list):
            for item in reversed(data):
                dt = self._extract_time_from_any(item)
                if dt:
                    return dt

        # 常见结构 2：字典，包含 messages 列表
        if isinstance(data, dict):
            # 尝试 messages 列表
            messages = data.get("messages") or data.get(
                "history") or data.get("items")
            if isinstance(messages, list):
                for item in reversed(messages):
                    dt = self._extract_time_from_any(item)
                    if dt:
                        return dt
            # 尝试直接从字典中取时间字段
            dt = self._extract_time_from_any(data)
            if dt:
                return dt

        return None

    def _last_time_from_txt(self, path: str) -> Optional[datetime]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
            for line in reversed(lines):
                dt = self._parse_datetime_value(line)
                if dt:
                    return dt
        except Exception:
            return None
        return None

    def _extract_time_from_any(self, obj: Any) -> Optional[datetime]:
        # 若是字符串，尝试解析
        if isinstance(obj, str):
            # 尝试作为 JSON 行
            try:
                obj = json.loads(obj)
            except Exception:
                return self._parse_datetime_value(obj)

        if isinstance(obj, dict):
            # 常见时间字段名
            candidates = [
                "time",
                "timestamp",
                "created_at",
                "updated_at",
                "datetime",
                "date",
                "ts",
            ]
            for key in candidates:
                if key in obj:
                    dt = self._parse_datetime_value(obj[key])
                    if dt:
                        return dt

            # 嵌套字段
            nested = obj.get("meta") or obj.get("extra") or obj.get("header")
            if isinstance(nested, dict):
                dt = self._extract_time_from_any(nested)
                if dt:
                    return dt

        return None

    def _parse_datetime_value(self, value: Any) -> Optional[datetime]:
        if value is None:
            return None

        if isinstance(value, datetime):
            return value

        if isinstance(value, (int, float)):
            try:
                # 处理可能是毫秒时间戳
                ts = float(value)
                if ts > 1e12:  # 毫秒
                    ts /= 1000.0
                return datetime.fromtimestamp(ts)
            except Exception:
                return None

        if isinstance(value, str):
            s = value.strip()
            if not s:
                return None

            # ISO8601
            iso = s.replace("Z", "+00:00")
            try:
                # Python 3.11+ 兼容多种 ISO 格式
                dt = datetime.fromisoformat(iso)
                return dt
            except Exception:
                pass

            # 常见格式尝试
            fmts = [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d %H:%M",
                "%Y/%m/%d %H:%M:%S",
                "%Y/%m/%d %H:%M",
                "%Y-%m-%d",
                "%Y/%m/%d",
                "%Y%m%d%H%M%S",
                "%Y%m%d%H%M",
                "%Y%m%d",
            ]
            for fmt in fmts:
                try:
                    return datetime.strptime(s, fmt)
                except Exception:
                    continue

            # 尝试将纯数字字符串作为时间戳
            if s.isdigit():
                try:
                    ts = int(s)
                    if ts > 1e12:
                        ts = ts // 1000
                    return datetime.fromtimestamp(ts)
                except Exception:
                    return None

        return None
