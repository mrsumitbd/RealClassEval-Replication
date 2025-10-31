
from dataclasses import dataclass, field
import time


@dataclass
class SuperChatRecord:
    user_id: int
    message: str
    amount: float
    timestamp: float  # Unix timestamp when the superchat was sent
    duration: float   # Duration in seconds for which the superchat is valid

    def is_expired(self) -> bool:
        return (time.time() - self.timestamp) >= self.duration

    def remaining_time(self) -> float:
        remaining = self.duration - (time.time() - self.timestamp)
        return max(0.0, remaining)

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "message": self.message,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "duration": self.duration,
            "is_expired": self.is_expired(),
            "remaining_time": self.remaining_time()
        }
