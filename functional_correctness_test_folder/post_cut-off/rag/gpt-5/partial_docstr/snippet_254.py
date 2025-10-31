import os
import json
from typing import Optional, List
from datetime import datetime


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
        candidates: List[str] = [
            os.path.join(self.history_dir, f'{character_id}.jsonl'),
            os.path.join(self.history_dir, f'{character_id}.json'),
            os.path.join(self.history_dir, f'{character_id}.md'),
            os.path.join(self.history_dir, f'{character_id}.txt'),
        ]
        for path in candidates:
            if os.path.isfile(path):
                return path
        # 默认返回 .jsonl 路径（即便文件不存在，调用方可以据此写入）
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
            # 若存在以角色ID命名的目录，则查找其中最新修改时间
            dir_path = os.path.join(self.history_dir, character_id)
            if os.path.isdir(dir_path):
                latest_mtime = None
                for root, _, files in os.walk(dir_path):
                    for f in files:
                        fp = os.path.join(root, f)
                        try:
                            mtime = os.path.getmtime(fp)
                        except OSError:
                            continue
                        if latest_mtime is None or mtime > latest_mtime:
                            latest_mtime = mtime
                if latest_mtime is not None:
                    return datetime.fromtimestamp(latest_mtime)
            return None

        # 尝试从内容中解析最后一条消息时间
        last_time = self._parse_last_time_from_file(path)
        if last_time is not None:
            return last_time

        # 回退为文件最后修改时间
        try:
            return datetime.fromtimestamp(os.path.getmtime(path))
        except OSError:
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
            return '首次对话'
        delta = current_time - last_time
        seconds = int(delta.total_seconds())
        if seconds < 0:
            seconds = 0

        if seconds < 60:
            return f'{seconds}秒'
        minutes = seconds // 60
        if minutes < 60:
            return f'{minutes}分钟'
        hours = minutes // 60
        if hours < 24:
            return f'{hours}小时'
        days = hours // 24
        if days < 30:
            return f'{days}天'
        months = days // 30
        if months < 12:
            return f'{months}个月'
        years = months // 12
        return f'{years}年'

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
        if last_time is None:
            return '首次对话'
        elapsed_str = self.format_time_elapsed(last_time, now)
        return f'距上次对话{elapsed_str}'

    # -------------------- 内部工具方法 --------------------

    def _parse_last_time_from_file(self, path: str) -> Optional[datetime]:
        # 优先尝试逐行反向读取（jsonl 或按行日志）
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except OSError:
            return None

        # 反向遍历，找到最后一个可解析的时间
        for line in reversed(lines):
            line = line.strip()
            if not line:
                continue
            # 尝试 JSON
            ts = self._parse_time_from_json_line(line)
            if ts is not None:
                return ts
            # 尝试从纯文本中提取时间（简单兜底：不实现复杂解析）
            # 由于格式未知，放弃从非JSON文本中解析，留给文件mtime兜底
        return None

    def _parse_time_from_json_line(self, line: str) -> Optional[datetime]:
        try:
            obj = json.loads(line)
        except Exception:
            return None

        # 常见时间字段候选
        candidates = ['timestamp', 'time',
                      'datetime', 'created_at', 'created', 'ts']
        for key in candidates:
            if key in obj:
                parsed = self._parse_time_value(obj[key])
                if parsed is not None:
                    return parsed
        # 嵌套结构尝试：message/time, meta/time 等
        nested_paths = [
            ('message', 'time'),
            ('meta', 'time'),
            ('data', 'time'),
            ('message', 'timestamp'),
            ('meta', 'timestamp'),
            ('data', 'timestamp'),
        ]
        for a, b in nested_paths:
            if isinstance(obj.get(a), dict) and b in obj[a]:
                parsed = self._parse_time_value(obj[a][b])
                if parsed is not None:
                    return parsed
        return None

    def _parse_time_value(self, value) -> Optional[datetime]:
        # 数值：epoch 秒/毫秒
        if isinstance(value, (int, float)):
            ts = float(value)
            # 毫秒判断
            if ts > 1e12:
                ts /= 1000.0
            try:
                return datetime.fromtimestamp(ts)
            except (OverflowError, OSError, ValueError):
                return None

        if isinstance(value, str):
            s = value.strip()
            # 兼容 ISO8601 的 Z 时区
            if s.endswith('Z'):
                s = s[:-1] + '+00:00'
            # 尝试 fromisoformat
            try:
                return datetime.fromisoformat(s)
            except ValueError:
                pass
            # 尝试常见格式
            fmts = [
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d %H:%M',
                '%Y/%m/%d %H:%M:%S',
                '%Y/%m/%d %H:%M',
                '%Y-%m-%dT%H:%M:%S',
                '%Y-%m-%dT%H:%M:%S.%f',
                '%Y-%m-%d',
                '%Y/%m/%d',
            ]
            for fmt in fmts:
                try:
                    return datetime.strptime(s, fmt)
                except ValueError:
                    continue
        return None
