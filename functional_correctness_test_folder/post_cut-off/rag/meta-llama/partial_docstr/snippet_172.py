
from dataclasses import dataclass, asdict
import time
from typing import Optional


@dataclass
class SuperChatRecord:
    """SuperChat记录数据类"""
    price: float
    """SuperChat价格"""
    message: str
    """SuperChat消息内容"""
    timestamp: float
    """SuperChat时间戳（秒）"""
    duration: int
    """SuperChat持续时间（秒）"""

    def is_expired(self) -> bool:
        """检查SuperChat是否已过期"""
        return time.time() - self.timestamp > self.duration

    def remaining_time(self) -> float:
        """获取剩余时间（秒）"""
        return max(0, self.timestamp + self.duration - time.time())

    def to_dict(self) -> dict:
        """转换为字典格式"""
        return asdict(self)
