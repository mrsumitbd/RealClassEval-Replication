
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta


@dataclass
class SuperChatRecord:
    """Represents a Super Chat record."""
    amount: float
    currency: str
    timestamp: datetime
    expiration_time: datetime

    def is_expired(self) -> bool:
        """Checks if the Super Chat has expired."""
        return self.expiration_time < datetime.now()

    def remaining_time(self) -> float:
        """Calculates the remaining time until the Super Chat expires."""
        if self.is_expired():
            return 0.0
        return (self.expiration_time - datetime.now()).total_seconds()

    def to_dict(self) -> dict:
        """Converts the Super Chat record to a dictionary."""
        data = asdict(self)
        data['timestamp'] = data['timestamp'].isoformat()
        data['expiration_time'] = data['expiration_time'].isoformat()
        return data


# Example usage:
if __name__ == "__main__":
    record = SuperChatRecord(
        amount=10.99,
        currency='USD',
        timestamp=datetime.now(),
        expiration_time=datetime.now() + timedelta(hours=1)
    )
    print(record.is_expired())
    print(record.remaining_time())
    print(record.to_dict())
