
from dataclasses import dataclass, asdict
import time
from typing import Optional


@dataclass
class SuperChatRecord:
    """SuperChat记录数据类"""
    user_id: str
    message: str
    price: float
    timestamp: float
    expire_time: float

    def is_expired(self) -> bool:
        """检查SuperChat是否已过期"""
        return time.time() > self.expire_time

    def remaining_time(self) -> float:
        """获取剩余时间（秒）"""
        return max(0, self.expire_time - time.time())

    def to_dict(self) -> dict:
        """转换为字典格式"""
        return asdict(self)
