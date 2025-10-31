
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict


@dataclass
class SuperChatRecord:
    """SuperChat记录数据类"""

    # 记录开始时间（UTC）
    start_time: datetime = field(default_factory=datetime.utcnow)
    # 记录持续时间（秒）
    duration: int = 0
    # 其它可选字段（如金额、用户等）
    amount: float | None = None
    user_id: str | None = None
    # 记录唯一标识
    record_id: str | None = None

    def is_expired(self) -> bool:
        """检查SuperChat是否已过期"""
        end_time = self.start_time + timedelta(seconds=self.duration)
        return datetime.utcnow() >= end_time

    def remaining_time(self) -> float:
        """获取剩余时间（秒）"""
        end_time = self.start_time + timedelta(seconds=self.duration)
        remaining = (end_time - datetime.utcnow()).total_seconds()
        return max(0.0, remaining)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "record_id": self.record_id,
            "start_time": self.start_time.isoformat(),
            "duration": self.duration,
            "amount": self.amount,
            "user_id": self.user_id,
        }
