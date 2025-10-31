from dataclasses import dataclass, field, asdict
import time


@dataclass
class SuperChatRecord:
    '''SuperChat记录数据类'''
    uid: int
    uname: str
    message: str
    price: float
    duration: float  # seconds
    start_time: float = field(default_factory=time.time)

    def is_expired(self) -> bool:
        now = time.time()
        return now >= self.start_time + max(0.0, self.duration)

    def remaining_time(self) -> float:
        now = time.time()
        remaining = self.start_time + max(0.0, self.duration) - now
        return remaining if remaining > 0 else 0.0

    def to_dict(self) -> dict:
        data = asdict(self)
        data.update({
            "expired": self.is_expired(),
            "remaining_time": self.remaining_time(),
        })
        return data
