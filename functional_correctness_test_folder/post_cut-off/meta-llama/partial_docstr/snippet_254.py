
import os
import datetime
from typing import Optional


class TimeTracker:

    def __init__(self, history_dir: str):
        '''
        初始化时间跟踪器
        Args:
            history_dir: 历史记录存储目录
        '''
        self.history_dir = history_dir
        if not os.path.exists(history_dir):
            os.makedirs(history_dir)

    def _get_character_history_file(self, character_id: str) -> str:
        '''
        获取角色历史记录文件路径
        Args:
            character_id: 角色ID
        Returns:
            历史记录文件路径
        '''
        return os.path.join(self.history_dir, f'{character_id}.txt')

    def get_last_message_time(self, character_id: str) -> Optional[datetime.datetime]:
        history_file = self._get_character_history_file(character_id)
        if not os.path.exists(history_file):
            return None
        with open(history_file, 'r') as f:
            last_time_str = f.read().strip()
            if last_time_str:
                return datetime.datetime.strptime(last_time_str, '%Y-%m-%d %H:%M:%S')
        return None

    def format_time_elapsed(self, last_time: Optional[datetime.datetime], current_time: datetime.datetime) -> str:
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
        time_diff = current_time - last_time
        days = time_diff.days
        hours, remainder = divmod(time_diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if days > 0:
            return f'{days}天{hours}小时前'
        elif hours > 0:
            return f'{hours}小时{minutes}分钟前'
        elif minutes > 0:
            return f'{minutes}分钟{seconds}秒前'
        else:
            return f'{seconds}秒前'

    def get_time_elapsed_prefix(self, character_id: str) -> str:
        '''
        获取时间间隔前缀
        Args:
            character_id: 角色ID
        Returns:
            时间间隔前缀，如"距上次对话xx"
        '''
        last_time = self.get_last_message_time(character_id)
        current_time = datetime.datetime.now()
        time_elapsed_str = self.format_time_elapsed(last_time, current_time)
        if last_time is not None:
            with open(self._get_character_history_file(character_id), 'w') as f:
                f.write(current_time.strftime('%Y-%m-%d %H:%M:%S'))
        return f'距上次对话{time_elapsed_str}'
