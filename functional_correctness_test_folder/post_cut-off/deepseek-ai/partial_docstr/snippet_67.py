
from dataclasses import dataclass, asdict
import time


@dataclass
class SuperChatRecord:
    '''SuperChat记录数据类'''

    def is_expired(self) -> bool:
        return self.remaining_time() <= 0

    def remaining_time(self) -> float:
        '''获取剩余时间（秒）'''
        return 0.0

    def to_dict(self) -> dict:
        return asdict(self)
