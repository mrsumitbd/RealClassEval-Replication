from dataclasses import dataclass, asdict, field
from typing import Optional
import time


@dataclass
class SuperChatRecord:
    '''SuperChat记录数据类'''
    user_id: str
    message: str
    amount: float
    start_time: float  # Unix timestamp
    duration: float    # seconds
    extra: Optional[dict] = field(default_factory=dict)

    def is_expired(self) -> bool:
        '''检查SuperChat是否已过期'''
        return time.time() >= self.start_time + self.duration

    def remaining_time(self) -> float:
        '''获取剩余时间（秒）'''
        remain = (self.start_time + self.duration) - time.time()
        return max(0.0, remain)

    def to_dict(self) -> dict:
        '''转换为字典格式'''
        return asdict(self)
