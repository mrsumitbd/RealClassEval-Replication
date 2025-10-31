
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class SuperChatRecord:
    created_at: datetime
    expires_at: datetime
    message: str = ""

    def is_expired(self) -> bool:
        return datetime.now() >= self.expires_at

    def remaining_time(self) -> float:
        remaining = (self.expires_at - datetime.now()).total_seconds()
        return max(0.0, remaining)

    def to_dict(self) -> dict:
        return {
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat(),
            "message": self.message,
            "is_expired": self.is_expired(),
            "remaining_time": self.remaining_time(),
        }
