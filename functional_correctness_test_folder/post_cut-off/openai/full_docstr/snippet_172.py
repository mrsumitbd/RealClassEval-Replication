
from dataclasses import dataclass, field
import time
from typing import Dict


@dataclass
class SuperChatRecord:
    """SuperChat记录数据类"""

    # 开始时间（Unix 时间戳，秒）
    start_time: float = field(default_factory=time.time)
    # 持续时间（秒）
    duration: float = 0.0

    def is_expired(self) -> bool:
        """检查SuperChat是否已过期"""
        return time.time() >= self.start_time + self.duration

    def remaining_time(self) -> float:
        """获取剩余时间（秒）"""
        remaining = (self.start_time + self.duration) - time.time()
        return max(0.0, remaining)

    def to_dict(self) -> Dict[str, float]:
        """转换为字典格式"""
        return {
            "start_time": self.start_time,
            "duration": self.duration,
            "expired": self.is_expired(),
            "remaining_time": self.remaining_time(),
        }
