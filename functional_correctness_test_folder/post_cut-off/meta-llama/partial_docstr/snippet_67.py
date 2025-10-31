
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class SuperChatRecord:
    '''SuperChat记录数据类'''
    id: int
    price: float
    message: str
    start_time: datetime
    end_time: datetime

    def is_expired(self) -> bool:
        return datetime.now() > self.end_time

    def remaining_time(self) -> float:
        '''获取剩余时间（秒）'''
        if self.is_expired():
            return 0.0
        return (self.end_time - datetime.now()).total_seconds()

    def to_dict(self) -> dict:
        return asdict(self)
