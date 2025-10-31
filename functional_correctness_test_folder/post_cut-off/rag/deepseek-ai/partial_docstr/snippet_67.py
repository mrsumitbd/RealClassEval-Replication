
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


@dataclass
class SuperChatRecord:
    '''SuperChat记录数据类'''
    amount: float
    currency: str
    message: str
    start_time: datetime
    duration: float  # in seconds

    def is_expired(self) -> bool:
        '''检查SuperChat是否已过期'''
        elapsed = (datetime.now() - self.start_time).total_seconds()
        return elapsed >= self.duration

    def remaining_time(self) -> float:
        '''获取剩余时间（秒）'''
        elapsed = (datetime.now() - self.start_time).total_seconds()
        return max(0.0, self.duration - elapsed)

    def to_dict(self) -> dict:
        '''转换为字典格式'''
        return asdict(self)
