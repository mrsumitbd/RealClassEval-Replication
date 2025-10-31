
from dataclasses import dataclass, asdict
import time


@dataclass
class SuperChatRecord:
    '''SuperChat记录数据类'''
    timestamp: float
    duration: float
    amount: float
    currency: str
    message: str

    def is_expired(self) -> bool:
        return time.time() > self.timestamp + self.duration

    def remaining_time(self) -> float:
        remaining = (self.timestamp + self.duration) - time.time()
        return max(0.0, remaining)

    def to_dict(self) -> dict:
        return asdict(self)
