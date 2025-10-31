from dataclasses import dataclass, field, asdict
from typing import Optional, Any, Dict
import time


@dataclass
class SuperChatRecord:
    user_id: Optional[str] = None
    message: str = ""
    amount: float = 0.0
    currency: str = "USD"
    created_at: float = field(default_factory=lambda: time.time())
    duration: float = 0.0  # seconds

    def is_expired(self) -> bool:
        end_time = self.created_at + max(0.0, self.duration)
        return time.time() >= end_time

    def remaining_time(self) -> float:
        end_time = self.created_at + max(0.0, self.duration)
        return max(0.0, end_time - time.time())

    def to_dict(self) -> dict:
        data: Dict[str, Any] = asdict(self)
        data.update(
            {
                "expired": self.is_expired(),
                "remaining_time": self.remaining_time(),
            }
        )
        return data
