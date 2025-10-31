
from dataclasses import dataclass, asdict, field
import time


@dataclass
class SuperChatRecord:
    '''SuperChat记录数据类'''
    user_id: int
    message: str
    amount: float
    start_time: float  # timestamp
    duration: float    # seconds

    def is_expired(self) -> bool:
        return (time.time() - self.start_time) >= self.duration

    def remaining_time(self) -> float:
        remaining = self.start_time + self.duration - time.time()
        return max(0.0, remaining)

    def to_dict(self) -> dict:
        return asdict(self)
