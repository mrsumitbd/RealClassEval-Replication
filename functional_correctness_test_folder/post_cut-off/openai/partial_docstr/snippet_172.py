
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import Dict, Any


@dataclass
class SuperChatRecord:
    """SuperChat记录数据类"""

    # 开始时间（UTC）
    start_time: datetime
    # 持续时间（秒）
    duration: float

    def is_expired(self) -> bool:
        """判断 SuperChat 是否已过期"""
        now = datetime.utcnow()
        end_time = self.start_time + timedelta(seconds=self.duration)
        return now >= end_time

    def remaining_time(self) -> float:
        """返回剩余时间（秒），若已过期则返回 0"""
        now = datetime.utcnow()
        end_time = self.start_time + timedelta(seconds=self.duration)
        remaining = (end_time - now).total_seconds()
        return max(0.0, remaining)

    def to_dict(self) -> Dict[str, Any]:
        """将记录转换为字典，时间字段以 ISO 格式字符串表示"""
        data = asdict(self)
        data["start_time"] = self.start_time.isoformat()
        return data
