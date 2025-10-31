from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import time


@dataclass
class SuperChatRecord:
    '''SuperChat记录数据类'''
    created_at: float = field(default_factory=lambda: time.time())
    duration: Optional[float] = None
    expire_at: Optional[float] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.duration is not None:
            self.duration = float(self.duration)
            if self.duration < 0:
                self.duration = 0.0
        if self.expire_at is not None:
            self.expire_at = float(self.expire_at)
        self.created_at = float(self.created_at)

        if self.expire_at is None and self.duration is not None:
            self.expire_at = self.created_at + self.duration
        elif self.expire_at is None and self.duration is None:
            raise ValueError(
                "Either 'duration' or 'expire_at' must be provided.")

    def _expiry_time(self) -> float:
        return float(self.expire_at) if self.expire_at is not None else self.created_at

    def is_expired(self) -> bool:
        '''检查SuperChat是否已过期'''
        return time.time() >= self._expiry_time()

    def remaining_time(self) -> float:
        '''获取剩余时间（秒）'''
        remaining = self._expiry_time() - time.time()
        return remaining if remaining > 0 else 0.0

    def to_dict(self) -> dict:
        '''转换为字典格式'''
        return {
            'created_at': self.created_at,
            'duration': self.duration,
            'expire_at': self.expire_at,
            'expired': self.is_expired(),
            'remaining_time': self.remaining_time(),
            'extra': self.extra.copy(),
        }
