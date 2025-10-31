from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any
import time


@dataclass
class SuperChatRecord:
    '''SuperChat记录数据类'''

    sc_id: Optional[str] = None
    user_id: Optional[int] = None
    user_name: Optional[str] = None
    message: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    start_ts: float = field(default_factory=lambda: time.time())
    duration: float = 0.0  # 秒

    def is_expired(self) -> bool:
        '''检查SuperChat是否已过期'''
        return self.remaining_time() <= 0.0

    def remaining_time(self) -> float:
        '''获取剩余时间（秒）'''
        now = time.time()
        end_ts = self.start_ts + max(0.0, self.duration)
        return max(0.0, end_ts - now)

    def to_dict(self) -> dict:
        '''转换为字典格式'''
        data: Dict[str, Any] = asdict(self)
        data["remaining_time"] = self.remaining_time()
        data["expired"] = self.is_expired()
        return data
