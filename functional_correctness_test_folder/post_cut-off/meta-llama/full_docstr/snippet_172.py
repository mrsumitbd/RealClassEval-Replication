
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta


@dataclass
class SuperChatRecord:
    '''SuperChat记录数据类'''
    id: int
    price: float
    message: str
    start_time: datetime
    timeout: int  # in seconds

    def is_expired(self) -> bool:
        '''检查SuperChat是否已过期'''
        return datetime.now() > self.start_time + timedelta(seconds=self.timeout)

    def remaining_time(self) -> float:
        '''获取剩余时间（秒）'''
        remaining = self.start_time + \
            timedelta(seconds=self.timeout) - datetime.now()
        return max(remaining.total_seconds(), 0)

    def to_dict(self) -> dict:
        '''转换为字典格式'''
        data = asdict(self)
        data['start_time'] = self.start_time.isoformat()
        return data
