from dataclasses import dataclass, field, asdict
from typing import Optional
import time


@dataclass
class SuperChatRecord:
    '''SuperChat记录数据类'''
    user_id: Optional[int] = None
    username: Optional[str] = None
    message: str = ""
    amount: float = 0.0
    currency: str = "CNY"
    start_time: float = field(default_factory=lambda: time.time())
    duration: float = 0.0  # 秒

    def is_expired(self) -> bool:
        return time.time() >= self.start_time + self.duration

    def remaining_time(self) -> float:
        '''获取剩余时间（秒）'''
        remaining = self.start_time + self.duration - time.time()
        return remaining if remaining > 0 else 0.0

    def to_dict(self) -> dict:
        return asdict(self)
