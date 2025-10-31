
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class SuperChatRecord:
    '''SuperChat记录数据类'''
    amount: float
    message: str
    timestamp: datetime
    duration: timedelta

    def is_expired(self) -> bool:
        expiration_time = self.timestamp + self.duration
        return datetime.now() > expiration_time

    def remaining_time(self) -> float:
        expiration_time = self.timestamp + self.duration
        remaining = expiration_time - datetime.now()
        return remaining.total_seconds() if remaining.total_seconds() > 0 else 0.0

    def to_dict(self) -> dict:
        return {
            'amount': self.amount,
            'message': self.message,
            'timestamp': self.timestamp.isoformat(),
            'duration': self.duration.total_seconds()
        }
