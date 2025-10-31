from dataclasses import dataclass, field, asdict
import time


@dataclass
class SuperChatRecord:
    '''SuperChat记录数据类'''
    start_time: float = field(default_factory=lambda: time.time())
    duration: float = 0.0  # 持续时间（秒）

    def is_expired(self) -> bool:
        '''检查SuperChat是否已过期'''
        if self.duration <= 0:
            return True
        return (self.start_time + self.duration) <= time.time()

    def remaining_time(self) -> float:
        '''获取剩余时间（秒）'''
        if self.duration <= 0:
            return 0.0
        remaining = (self.start_time + self.duration) - time.time()
        return remaining if remaining > 0 else 0.0

    def to_dict(self) -> dict:
        '''转换为字典格式'''
        return asdict(self)
