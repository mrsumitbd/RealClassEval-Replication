from typing import Any, Dict, Mapping, Optional, Tuple, Type, Union
import datetime

class RateLimit:
    """The rate limit imposed upon the requester.

    The 'limit' attribute specifies the rate of requests per hour the client is
    limited to.

    The 'remaining' attribute specifies how many requests remain within the
    current rate limit that the client can make.

    The reset_datetime attribute is a datetime object representing when
    effectively 'left' resets to 'rate'. The datetime object is timezone-aware
    and set to UTC.

    The boolean value of an instance whether another request can be made. This
    is determined based on whether there are any remaining requests or if the
    reset datetime has passed.
    """

    def __init__(self, *, limit: int, remaining: int, reset_epoch: float) -> None:
        """Instantiate a RateLimit object.

        The reset_epoch argument should be in seconds since the UTC epoch.
        """
        self.limit = limit
        self.remaining = remaining
        self.reset_datetime = datetime.datetime.fromtimestamp(reset_epoch, datetime.timezone.utc)

    def __bool__(self) -> bool:
        """True if requests are remaining or the reset datetime has passed."""
        if self.remaining > 0:
            return True
        else:
            now = datetime.datetime.now(datetime.timezone.utc)
            return now > self.reset_datetime

    def __str__(self) -> str:
        """Provide all details in a reasonable format."""
        return f'< {self.remaining:,}/{self.limit:,} until {self.reset_datetime} >'

    @classmethod
    def from_http(cls, headers: Mapping[str, str]) -> Optional['RateLimit']:
        """Gather rate limit information from HTTP headers.

        The mapping providing the headers is expected to support lowercase
        keys.  Returns ``None`` if ratelimit info is not found in the headers.
        """
        try:
            limit = int(headers['x-ratelimit-limit'])
            remaining = int(headers['x-ratelimit-remaining'])
            reset_epoch = float(headers['x-ratelimit-reset'])
        except KeyError:
            return None
        else:
            return cls(limit=limit, remaining=remaining, reset_epoch=reset_epoch)