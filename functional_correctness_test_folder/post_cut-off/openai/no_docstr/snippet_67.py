
from dataclasses import dataclass, asdict
import time


@dataclass
class SuperChatRecord:
    """
    Represents a record for a super chat with a start time and a duration.
    """
    start_time: float  # epoch timestamp when the chat becomes active
    duration: float    # duration in seconds for which the chat is valid

    def is_expired(self) -> bool:
        """
        Returns True if the current time is past the end of the chat duration.
        """
        return time.time() > self.start_time + self.duration

    def remaining_time(self) -> float:
        """
        Returns the remaining time in seconds until the chat expires.
        If already expired, returns 0.0.
        """
        remaining = (self.start_time + self.duration) - time.time()
        return max(0.0, remaining)

    def to_dict(self) -> dict:
        """
        Serialises the record to a plain dictionary.
        """
        return asdict(self)
