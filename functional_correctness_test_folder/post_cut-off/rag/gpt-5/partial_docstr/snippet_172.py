from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any


@dataclass
class SuperChatRecord:
    '''SuperChat记录数据类'''
    id: Optional[str] = None
    user_id: Optional[str] = None
    user_name: Optional[str] = None
    message: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    started_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc))
    duration_seconds: float = 0.0
    extra: Dict[str, Any] = field(default_factory=dict)

    def is_expired(self) -> bool:
        '''检查SuperChat是否已过期'''
        start = self.started_at if self.started_at.tzinfo else self.started_at.replace(
            tzinfo=timezone.utc)
        end = start + timedelta(seconds=max(0.0, self.duration_seconds))
        now = datetime.now(timezone.utc)
        return now >= end

    def remaining_time(self) -> float:
        '''获取剩余时间（秒）'''
        start = self.started_at if self.started_at.tzinfo else self.started_at.replace(
            tzinfo=timezone.utc)
        end = start + timedelta(seconds=max(0.0, self.duration_seconds))
        remaining = (end - datetime.now(timezone.utc)).total_seconds()
        return remaining if remaining > 0 else 0.0

    def to_dict(self) -> dict:
        '''转换为字典格式'''
        data = asdict(self)
        start = self.started_at if self.started_at.tzinfo else self.started_at.replace(
            tzinfo=timezone.utc)
        data['started_at'] = start.isoformat()
        data['expired'] = self.is_expired()
        data['remaining_time'] = self.remaining_time()
        return data
