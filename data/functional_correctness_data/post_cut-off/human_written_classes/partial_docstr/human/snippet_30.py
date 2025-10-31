from dataclasses import dataclass
import time
from typing import Any, Optional

@dataclass
class CacheEntry:
    """缓存条目数据结构"""
    value: Any
    timestamp: float
    ttl: Optional[float] = None
    access_count: int = 0
    last_access: float = None

    def __post_init__(self):
        if self.last_access is None:
            self.last_access = self.timestamp

    def is_expired(self) -> bool:
        """检查是否过期"""
        if self.ttl is None:
            return False
        return time.time() - self.timestamp > self.ttl

    def touch(self):
        """更新访问时间和计数"""
        self.last_access = time.time()
        self.access_count += 1