
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Any


@dataclass
class SuperChatRecord:
    """SuperChat记录数据类"""

    # 记录开始时间（UTC）
    start_time: datetime
    # 记录结束时间（UTC）
    end_time: datetime

    def is_expired(self) -> bool:
        """检查SuperChat是否已过期"""
        now = datetime.now(timezone.utc)
        return now >= self.end_time

    def remaining_time(self) -> float:
        """获取剩余时间（秒）"""
        now = datetime.now(timezone.utc)
        delta = self.end_time - now
        return max(delta.total_seconds(), 0.0)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "is_expired": self.is_expired(),
            "remaining_time": self.remaining_time(),
        }
