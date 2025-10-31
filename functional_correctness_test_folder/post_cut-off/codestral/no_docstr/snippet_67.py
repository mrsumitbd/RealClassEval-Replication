
from dataclasses import dataclass
import time


@dataclass
class SuperChatRecord:
    amount: float
    currency: str
    message: str
    timestamp: float
    duration: float

    def is_expired(self) -> bool:
        current_time = time.time()
        return current_time > self.timestamp + self.duration

    def remaining_time(self) -> float:
        current_time = time.time()
        remaining = self.timestamp + self.duration - current_time
        return remaining if remaining > 0 else 0.0

    def to_dict(self) -> dict:
        return {
            'amount': self.amount,
            'currency': self.currency,
            'message': self.message,
            'timestamp': self.timestamp,
            'duration': self.duration
        }
