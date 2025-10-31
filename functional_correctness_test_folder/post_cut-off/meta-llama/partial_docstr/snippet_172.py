
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class SuperChatRecord:
    '''SuperChat记录数据类'''
    price: float
    start_time: datetime
    end_time: datetime
    message: str
    user_name: str

    def is_expired(self) -> bool:
        return datetime.now() > self.end_time

    def remaining_time(self) -> float:
        return max(0, (self.end_time - datetime.now()).total_seconds())

    def to_dict(self) -> dict:
        return asdict(self)
