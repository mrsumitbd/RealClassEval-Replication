
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class SuperChatRecord:
    '''SuperChat记录数据类'''
    amount: float
    currency: str
    message: str
    sender_name: str
    sender_id: str
    created_at: datetime = field(default_factory=datetime.now)
    duration: timedelta = field(default_factory=lambda: timedelta(hours=24))
    expired: bool = False

    def is_expired(self) -> bool:
        '''检查SuperChat是否已过期'''
        if self.expired:
            return True
        expiration_time = self.created_at + self.duration
        return datetime.now() > expiration_time

    def remaining_time(self) -> float:
        '''获取剩余时间（秒）'''
        if self.is_expired():
            return 0.0
        expiration_time = self.created_at + self.duration
        remaining = expiration_time - datetime.now()
        return remaining.total_seconds()

    def to_dict(self) -> dict:
        '''转换为字典格式'''
        return {
            'amount': self.amount,
            'currency': self.currency,
            'message': self.message,
            'sender_name': self.sender_name,
            'sender_id': self.sender_id,
            'created_at': self.created_at.isoformat(),
            'duration': self.duration.total_seconds(),
            'expired': self.is_expired()
        }
