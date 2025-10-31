
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class SuperChatRecord:
    '''SuperChat记录数据类'''
    amount: float
    currency: str
    message: str
    start_time: datetime
    duration: timedelta  # Duration in seconds

    def is_expired(self) -> bool:
        '''检查SuperChat是否已过期'''
        return datetime.now() > self.start_time + self.duration

    def remaining_time(self) -> float:
        '''获取剩余时间（秒）'''
        if self.is_expired():
            return 0.0
        return (self.start_time + self.duration - datetime.now()).total_seconds()

    def to_dict(self) -> dict:
        '''转换为字典格式'''
        return asdict(self)
