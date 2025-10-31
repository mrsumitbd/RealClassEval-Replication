import time

class ExpiringCache:
    """Simple cache with a deadline."""

    def __init__(self, seconds, timer=time.time):
        """C-tor."""
        self.duration = seconds
        self.timer = timer
        self.value = None
        self.set(None)

    def get(self):
        """Returns existing value, or None if deadline has expired."""
        if self.timer() > self.deadline:
            self.value = None
        return self.value

    def set(self, value):
        """Set new value and reset the deadline for expiration."""
        self.deadline = self.timer() + self.duration
        self.value = value