
from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class SuperChatRecord:
    '''SuperChat记录数据类'''
    amount: float
    currency: str
    start_time: datetime = field(default_factory=datetime.now)
    duration: int  # Duration in seconds

    def is_expired(self) -> bool:
        '''检查SuperChat是否已过期'''
        return datetime.now() > self.start_time + timedelta(seconds=self.duration)

    def remaining_time(self) -> float:
        '''获取剩余时间（秒）'''
        remaining = (self.start_time +
                     timedelta(seconds=self.duration)) - datetime.now()
        return remaining.total_seconds() if remaining.total_seconds() > 0 else 0.0

    def to_dict(self) -> dict:
        '''转换为字典格式'''
        return {
            'amount': self.amount,
            'currency': self.currency,
            'start_time': self.start_time.isoformat(),
            'duration': self.duration
        }
