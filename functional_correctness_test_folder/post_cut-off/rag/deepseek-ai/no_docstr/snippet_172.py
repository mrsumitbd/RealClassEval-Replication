
from dataclasses import dataclass, asdict
import time


@dataclass
class SuperChatRecord:
    '''SuperChat记录数据类'''
    start_time: float
    duration: float  # in seconds
    amount: float
    currency: str
    message: str

    def is_expired(self) -> bool:
        '''检查SuperChat是否已过期'''
        current_time = time.time()
        return current_time > self.start_time + self.duration

    def remaining_time(self) -> float:
        '''获取剩余时间（秒）'''
        current_time = time.time()
        remaining = (self.start_time + self.duration) - current_time
        return max(0.0, remaining)

    def to_dict(self) -> dict:
        '''转换为字典格式'''
        return asdict(self)
