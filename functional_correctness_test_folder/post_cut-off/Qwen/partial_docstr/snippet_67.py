
from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class SuperChatRecord:
    '''SuperChat记录数据类'''
    amount: float
    start_time: datetime
    duration: int  # in seconds

    def is_expired(self) -> bool:
        return datetime.now() > self.start_time + timedelta(seconds=self.duration)

    def remaining_time(self) -> float:
        '''获取剩余时间（秒）'''
        end_time = self.start_time + timedelta(seconds=self.duration)
        return max(0, (end_time - datetime.now()).total_seconds())

    def to_dict(self) -> dict:
        return {
            'amount': self.amount,
            'start_time': self.start_time.isoformat(),
            'duration': self.duration
        }
