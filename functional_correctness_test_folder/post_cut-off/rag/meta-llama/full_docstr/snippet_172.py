
from dataclasses import dataclass, asdict
import time
from typing import Optional


@dataclass
class SuperChatRecord:
    """SuperChat记录数据类"""
    price: float
    """SuperChat金额"""
    message: Optional[str] = None
    """SuperChat消息内容"""
    timestamp: float = None
    """SuperChat时间戳（秒）"""
    duration: float = 86400  # 默认有效期为1天（秒）
    """SuperChat有效期（秒）"""

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()

    def is_expired(self) -> bool:
        """检查SuperChat是否已过期"""
        return time.time() - self.timestamp > self.duration

    def remaining_time(self) -> float:
        """获取剩余时间（秒）"""
        return max(0, self.duration - (time.time() - self.timestamp))

    def to_dict(self) -> dict:
        """转换为字典格式"""
        return asdict(self)
