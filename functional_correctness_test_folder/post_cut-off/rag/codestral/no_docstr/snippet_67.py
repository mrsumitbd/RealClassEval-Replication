
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class SuperChatRecord:
    '''SuperChat记录数据类'''
    amount: float
    message: str
    sender_id: str
    created_at: datetime = field(default_factory=datetime.now)
    duration: timedelta = field(default_factory=lambda: timedelta(minutes=30))
    expired_at: Optional[datetime] = None

    def __post_init__(self):
        if self.expired_at is None:
            self.expired_at = self.created_at + self.duration

    def is_expired(self) -> bool:
        '''检查SuperChat是否已过期'''
        return datetime.now() > self.expired_at

    def remaining_time(self) -> float:
        '''获取剩余时间（秒）'''
        if self.is_expired():
            return 0.0
        remaining = self.expired_at - datetime.now()
        return remaining.total_seconds()

    def to_dict(self) -> dict:
        '''转换为字典格式'''
        return {
            'amount': self.amount,
            'message': self.message,
            'sender_id': self.sender_id,
            'created_at': self.created_at.isoformat(),
            'duration': self.duration.total_seconds(),
            'expired_at': self.expired_at.isoformat() if self.expired_at else None
        }
