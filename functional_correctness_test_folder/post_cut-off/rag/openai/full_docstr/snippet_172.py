
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import Any, Dict


@dataclass
class SuperChatRecord:
    """SuperChat记录数据类"""

    # 记录开始时间（UTC）
    start_time: datetime
    # 持续时间（秒）
    duration: int
    # 发送者 ID
    user_id: str
    # 发送金额
    amount: float

    def is_expired(self) -> bool:
        """检查SuperChat是否已过期"""
        now = datetime.utcnow()
        end_time = self.start_time + timedelta(seconds=self.duration)
        return now >= end_time

    def remaining_time(self) -> float:
        """获取剩余时间（秒）"""
        now = datetime.utcnow()
        end_time = self.start_time + timedelta(seconds=self.duration)
        remaining = (end_time - now).total_seconds()
        return max(0.0, remaining)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return asdict(self)
