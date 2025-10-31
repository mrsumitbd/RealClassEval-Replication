from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import time


@dataclass
class SuperChatRecord:
    '''SuperChat记录数据类'''
    user_id: Optional[int] = None
    message: str = ''
    price: float = 0.0
    start_time: float = field(default_factory=lambda: time.time())
    duration: float = 0.0  # 单位：秒
    extra: Dict[str, Any] = field(default_factory=dict)

    def is_expired(self) -> bool:
        '''检查SuperChat是否已过期'''
        return self.remaining_time() <= 0.0

    def remaining_time(self) -> float:
        '''获取剩余时间（秒）'''
        end_time = self.start_time + max(0.0, self.duration)
        return max(0.0, end_time - time.time())

    def to_dict(self) -> dict:
        '''转换为字典格式'''
        return {
            'user_id': self.user_id,
            'message': self.message,
            'price': self.price,
            'start_time': self.start_time,
            'duration': self.duration,
            'end_time': self.start_time + max(0.0, self.duration),
            'remaining_time': self.remaining_time(),
            'expired': self.is_expired(),
            'extra': dict(self.extra) if self.extra is not None else {},
        }
