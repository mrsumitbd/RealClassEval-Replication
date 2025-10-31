
from dataclasses import dataclass, asdict
import time


@dataclass
class SuperChatRecord:
    timestamp: float
    duration: float
    message: str
    sender: str

    def is_expired(self) -> bool:
        current_time = time.time()
        return current_time > self.timestamp + self.duration

    def remaining_time(self) -> float:
        current_time = time.time()
        remaining = (self.timestamp + self.duration) - current_time
        return max(0.0, remaining)

    def to_dict(self) -> dict:
        return asdict(self)
