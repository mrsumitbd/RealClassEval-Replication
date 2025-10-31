
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class SuperChatRecord:
    '''SuperChat记录数据类'''
    amount: float
    currency: str
    message: str
    sender_name: str
    sender_id: str
    start_time: datetime
    duration: timedelta

    def is_expired(self) -> bool:
        end_time = self.start_time + self.duration
        return datetime.now() > end_time

    def remaining_time(self) -> float:
        end_time = self.start_time + self.duration
        remaining = end_time - datetime.now()
        return remaining.total_seconds()

    def to_dict(self) -> dict:
        return {
            'amount': self.amount,
            'currency': self.currency,
            'message': self.message,
            'sender_name': self.sender_name,
            'sender_id': self.sender_id,
            'start_time': self.start_time.isoformat(),
            'duration': self.duration.total_seconds()
        }
