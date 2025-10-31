
from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class SuperChatRecord:
    start_time: datetime = field(default_factory=datetime.now)
    duration: timedelta = field(default_factory=lambda: timedelta(hours=1))

    def is_expired(self) -> bool:
        return datetime.now() > self.start_time + self.duration

    def remaining_time(self) -> float:
        remaining = (self.start_time + self.duration) - datetime.now()
        return remaining.total_seconds() if remaining.total_seconds() > 0 else 0.0

    def to_dict(self) -> dict:
        return {
            'start_time': self.start_time.isoformat(),
            'duration': self.duration.total_seconds()
        }
