
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class SuperChatRecord:
    '''SuperChat记录数据类'''
    message: str
    amount: float
    sender: str
    start_time: datetime
    duration: timedelta

    def is_expired(self) -> bool:
        '''检查SuperChat是否已过期'''
        return datetime.now() > self.start_time + self.duration

    def remaining_time(self) -> float:
        '''获取剩余时间（秒）'''
        if self.is_expired():
            return 0.0
        remaining = (self.start_time + self.duration -
                     datetime.now()).total_seconds()
        return max(remaining, 0.0)

    def to_dict(self) -> dict:
        '''转换为字典格式'''
        return {
            'message': self.message,
            'amount': self.amount,
            'sender': self.sender,
            'start_time': self.start_time.isoformat(),
            'duration': self.duration.total_seconds()
        }
