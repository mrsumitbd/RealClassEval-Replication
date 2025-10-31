import os
import json
from typing import Optional
from datetime import datetime, timezone


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

    def _get_character_history_file(self, character_id: str) -> str:
        '''
        获取角色历史记录文件路径
        Args:
            character_id: 角色ID
        Returns:
            历史记录文件路径
        '''
        # 优先返回已存在的文件，其次返回默认路径（.jsonl）
        candidates = [
            os.path.join(self.history_dir, f'{character_id}.jsonl'),
            os.path.join(self.history_dir, f'{character_id}.json'),
            os.path.join(self.history_dir, f'{character_id}.log'),
            os.path.join(self.history_dir, f'{character_id}.txt'),
        ]
        for path in candidates:
            if os.path.exists(path):
                return path
        return candidates[0]

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

        # 尝试从文件内容解析最后时间
        try:
            # 优先尝试按行JSON（jsonl）读取，若失败再尝试整体JSON
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            # 反向扫描最近的记录
            for line in reversed(lines):
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    dt = self._extract_datetime_from_obj(obj)
                    if dt is not None:
                        return dt
                except Exception:
                    continue

            # 尝试整体JSON
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                if content:
                    obj = json.loads(content)
                    # 如果是列表，反向查找
                    if isinstance(obj, list):
                        for item in reversed(obj):
                            dt = self._extract_datetime_from_obj(item)
                            if dt is not None:
                                return dt
                    else:
                        dt = self._extract_datetime_from_obj(obj)
                        if dt is not None:
                            return dt
            except Exception:
                pass

        except Exception:
            pass

        # 若未能解析到具体时间，回退到文件修改时间
        try:
            mtime = os.path.getmtime(path)
            return datetime.fromtimestamp(mtime, tz=timezone.utc)
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
            return '未知'

        last_utc = self._to_utc(last_time)
        curr_utc = self._to_utc(current_time)

        delta = curr_utc - last_utc
        total_seconds = int(delta.total_seconds())
        if total_seconds <= 0:
            return '刚刚'
        if total_seconds < 5:
            return '刚刚'

        minutes, seconds = divmod(total_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        parts = []
        if days:
            parts.append(f'{days}天')
        if hours:
            parts.append(f'{hours}小时')
        if minutes and len(parts) < 2:
            parts.append(f'{minutes}分钟')
        if not parts:
            parts.append(f'{seconds}秒')
        return ''.join(parts)

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
        if last is None:
            return '首次对话'
        span = self.format_time_elapsed(last, now)
        if span == '未知':
            return '首次对话'
        return f'距上次对话{span}'

    def _extract_datetime_from_obj(self, obj) -> Optional[datetime]:
        # 尝试从对象中提取时间字段
        # 支持的字段名
        keys = [
            'time', 'timestamp', 'created_at', 'createdAt', 'datetime', 'date',
            'created_time', 'update_time', 'updated_at', 'updatedAt'
        ]

        def parse_value(val) -> Optional[datetime]:
            dt = self._parse_datetime_value(val)
            if dt is not None:
                return dt
            return None

        if isinstance(obj, dict):
            # 直接字段
            for k in keys:
                if k in obj:
                    dt = parse_value(obj[k])
                    if dt:
                        return dt
            # 常见嵌套
            for nested_key in ['message', 'msg', 'meta', 'data', 'payload', 'info', 'content']:
                v = obj.get(nested_key)
                if v is not None:
                    dt = self._extract_datetime_from_obj(v)
                    if dt:
                        return dt
            # 递归所有值
            for v in obj.values():
                if isinstance(v, (dict, list)):
                    dt = self._extract_datetime_from_obj(v)
                    if dt:
                        return dt

        if isinstance(obj, list):
            for item in reversed(obj):
                dt = self._extract_datetime_from_obj(item)
                if dt:
                    return dt

        # 直接是时间值
        return self._parse_datetime_value(obj)

    def _parse_datetime_value(self, value) -> Optional[datetime]:
        if value is None:
            return None
        # 数字：时间戳（秒或毫秒）
        if isinstance(value, (int, float)):
            ts = float(value)
            # 大于1e12基本是毫秒
            if ts > 1e12:
                ts = ts / 1000.0
            try:
                return datetime.fromtimestamp(ts, tz=timezone.utc)
            except Exception:
                return None

        # 字符串：ISO8601 或常见格式
        if isinstance(value, str):
            s = value.strip()
            if not s:
                return None
            # 替换Z为+00:00
            if s.endswith('Z'):
                s = s[:-1] + '+00:00'
            # 尝试多种解析
            fmts = [
                None,  # 使用fromisoformat
                '%Y-%m-%d %H:%M:%S',
                '%Y/%m/%d %H:%M:%S',
                '%Y-%m-%d %H:%M',
                '%Y/%m/%d %H:%M',
                '%Y-%m-%d',
                '%Y/%m/%d',
            ]
            # 先fromisoformat
            try:
                dt = datetime.fromisoformat(s)
                return self._to_utc(dt)
            except Exception:
                pass
            # 再按格式尝试
            for fmt in fmts[1:]:
                try:
                    dt = datetime.strptime(s, fmt)
                    return self._to_utc(dt)
                except Exception:
                    continue
        return None

    def _to_utc(self, dt: datetime) -> datetime:
        if dt.tzinfo is None:
            local_tz = datetime.now().astimezone().tzinfo
            dt = dt.replace(tzinfo=local_tz)
        return dt.astimezone(timezone.utc)
