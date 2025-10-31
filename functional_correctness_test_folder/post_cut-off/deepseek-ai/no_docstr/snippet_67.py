
from dataclasses import dataclass
from time import time


@dataclass
class SuperChatRecord:
    timestamp: float
    duration: float
    message: str
    sender: str

    def is_expired(self) -> bool:
        return time() > self.timestamp + self.duration

    def remaining_time(self) -> float:
        return max(0.0, (self.timestamp + self.duration) - time())

    def to_dict(self) -> dict:
        return {
            'timestamp': self.timestamp,
            'duration': self.duration,
            'message': self.message,
            'sender': self.sender,
            'is_expired': self.is_expired(),
            'remaining_time': self.remaining_time()
        }
