from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any
import time


@dataclass
class SuperChatRecord:
    created_at: float = field(default_factory=time.time)
    ttl: float = 0.0
    expires_at: Optional[float] = None
    data: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.expires_at is None:
            self.expires_at = self.created_at + max(0.0, self.ttl)
        else:
            # Normalize values to be self-consistent
            self.ttl = max(0.0, self.expires_at - self.created_at)

    def is_expired(self) -> bool:
        now = time.time()
        return now >= (self.expires_at or now)

    def remaining_time(self) -> float:
        now = time.time()
        return max(0.0, (self.expires_at or now) - now)

    def to_dict(self) -> dict:
        return asdict(self)
