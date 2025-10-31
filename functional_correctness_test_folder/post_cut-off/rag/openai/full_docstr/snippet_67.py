
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict


@dataclass
class SuperChatRecord:
    """
    SuperChat记录数据类
    """
    # 记录开始时间（UTC）
    start_time: datetime
    # 超时持续时间（秒）
    duration: int
    # 付费金额（可选）
    amount: float = 0.0
    # 发送者用户 ID（可选）
    user_id: str = ""

    def is_expired(self) -> bool:
        """
        检查 SuperChat 是否已过期
        """
        return datetime.utcnow() > self.start_time + timedelta(seconds=self.duration)

    def remaining_time(self) -> float:
        """
        获取剩余时间（秒）
        """
        remaining = (self.start_time +
                     timedelta(seconds=self.duration)) - datetime.utcnow()
        return max(0.0, remaining.total_seconds())

    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典格式
        """
        return {
            "start_time": self.start_time.isoformat(),
            "duration": self.duration,
            "amount": self.amount,
            "user_id": self.user_id,
        }
