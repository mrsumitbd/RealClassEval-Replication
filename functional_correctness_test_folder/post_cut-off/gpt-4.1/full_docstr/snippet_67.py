
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta


@dataclass
class SuperChatRecord:
    '''SuperChat记录数据类'''
    user_id: int
    message: str
    amount: float
    start_time: datetime
    duration: float  # seconds

    def is_expired(self) -> bool:
        '''检查SuperChat是否已过期'''
        now = datetime.now()
        return now >= self.start_time + timedelta(seconds=self.duration)

    def remaining_time(self) -> float:
        '''获取剩余时间（秒）'''
        now = datetime.now()
        end_time = self.start_time + timedelta(seconds=self.duration)
        remaining = (end_time - now).total_seconds()
        return max(0.0, remaining)

    def to_dict(self) -> dict:
        '''转换为字典格式'''
        d = asdict(self)
        d['start_time'] = self.start_time.isoformat()
        d['is_expired'] = self.is_expired()
        d['remaining_time'] = self.remaining_time()
        return d
