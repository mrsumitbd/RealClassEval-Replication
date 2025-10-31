
from dataclasses import dataclass, asdict
import time


@dataclass
class SuperChatRecord:
    '''SuperChat记录数据类'''
    timestamp: float
    duration: float
    content: str
    user: str
    amount: float

    def is_expired(self) -> bool:
        '''检查SuperChat是否已过期'''
        current_time = time.time()
        return current_time > self.timestamp + self.duration

    def remaining_time(self) -> float:
        '''获取剩余时间（秒）'''
        current_time = time.time()
        remaining = (self.timestamp + self.duration) - current_time
        return max(0.0, remaining)

    def to_dict(self) -> dict:
        '''转换为字典格式'''
        return asdict(self)
