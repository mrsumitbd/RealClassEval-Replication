
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Dict, Any


@dataclass
class SuperChatRecord:
    """SuperChat记录数据类"""

    # 开始时间（UTC）
    start_time: datetime
    # 持续时间（秒）
    duration: int

    def is_expired(self) -> bool:
        """检查SuperChat是否已过期"""
        end_time = self.start_time + timedelta(seconds=self.duration)
        return datetime.now(timezone.utc) > end_time

    def remaining_time(self) -> float:
        """获取剩余时间（秒）"""
        end_time = self.start_time + timedelta(seconds=self.duration)
        remaining = end_time - datetime.now(timezone.utc)
        return max(0.0, remaining.total_seconds())

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "start_time": self.start_time.isoformat(),
            "duration": self.duration,
            "expired": self.is_expired(),
            "remaining_time": self.remaining_time(),
        }
