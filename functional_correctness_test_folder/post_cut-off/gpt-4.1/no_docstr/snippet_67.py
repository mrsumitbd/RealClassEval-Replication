
from dataclasses import dataclass, field
import time


@dataclass
class SuperChatRecord:
    user_id: int
    message: str
    amount: float
    created_at: float  # timestamp in seconds
    duration: float    # duration in seconds

    def is_expired(self) -> bool:
        return (time.time() - self.created_at) >= self.duration

    def remaining_time(self) -> float:
        remaining = self.duration - (time.time() - self.created_at)
        return max(0.0, remaining)

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "message": self.message,
            "amount": self.amount,
            "created_at": self.created_at,
            "duration": self.duration,
            "expired": self.is_expired(),
            "remaining_time": self.remaining_time()
        }
