from typing import Optional
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass

@dataclass(frozen=True)
class Credentials:
    """
    Represents credentials access key, secret key and session token.
    """
    access_key: str
    secret_key: str
    session_token: Optional[str] = None
    expiration: Optional[datetime] = None

    def __post_init__(self):
        if not self.access_key:
            raise ValueError('Access key must not be empty')
        if not self.secret_key:
            raise ValueError('Secret key must not be empty')
        if self.expiration and self.expiration.tzinfo:
            self.expiration = self.expiration.astimezone(timezone.utc).replace(tzinfo=None)

    def is_expired(self) -> bool:
        """Check whether this credentials expired or not."""
        return self.expiration < datetime.utcnow() + timedelta(seconds=10) if self.expiration else False