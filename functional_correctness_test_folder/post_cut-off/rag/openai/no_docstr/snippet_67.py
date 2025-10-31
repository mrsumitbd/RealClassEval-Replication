
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Any


@dataclass
class SuperChatRecord:
    """SuperChat记录数据类"""

    start_time: datetime  # 记录开始时间
    duration: int         # 持续时间（秒）

    def is_expired(self) -> bool:
        """检查SuperChat是否已过期"""
        return datetime.now() >= self.start_time + timedelta(seconds=self.duration)

    def remaining_time(self) -> float:
        """获取剩余时间（秒）"""
        remaining = (self.start_time +
                     timedelta(seconds=self.duration)) - datetime.now()
        return max(remaining.total_seconds(), 0.0)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "start_time": self.start_time.isoformat(),
            "duration": self.duration,
        }
