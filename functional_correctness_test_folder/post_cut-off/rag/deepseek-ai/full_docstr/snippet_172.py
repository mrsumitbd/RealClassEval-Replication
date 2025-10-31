
from dataclasses import dataclass
from typing import Dict, Any
import time


@dataclass
class SuperChatRecord:
    '''SuperChat记录数据类'''
    timestamp: float
    duration: float
    amount: float
    currency: str
    message: str

    def is_expired(self) -> bool:
        '''检查SuperChat是否已过期'''
        return time.time() > self.timestamp + self.duration

    def remaining_time(self) -> float:
        '''获取剩余时间（秒）'''
        remaining = (self.timestamp + self.duration) - time.time()
        return max(0.0, remaining) if not self.is_expired() else 0.0

    def to_dict(self) -> Dict[str, Any]:
        '''转换为字典格式'''
        return {
            'timestamp': self.timestamp,
            'duration': self.duration,
            'amount': self.amount,
            'currency': self.currency,
            'message': self.message,
            'is_expired': self.is_expired(),
            'remaining_time': self.remaining_time()
        }
