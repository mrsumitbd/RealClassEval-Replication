
import time


class ExpiringCache:
    def __init__(self, seconds, timer=time.time):
        self.seconds = seconds
        self.timer = timer
        self._value = None
        self._expires_at = None

    def set(self, value):
        """Store a value with an expiration time."""
        self._value = value
        self._expires_at = self.timer() + self.seconds

    def get(self):
        """Return the stored value if it hasn't expired, otherwise None."""
        if self._expires_at is None:
            return None
        if self.timer() < self._expires_at:
            return self._value
        # expired
        self._value = None
        self._expires_at = None
        return None
