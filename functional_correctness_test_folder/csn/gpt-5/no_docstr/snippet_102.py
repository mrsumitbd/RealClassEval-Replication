import time


class ExpiringCache:
    _MISSING = object()

    def __init__(self, seconds, timer=time.time):
        self._seconds = seconds
        self._timer = timer
        self._value = self._MISSING
        self._expires_at = None

    def get(self):
        if self._value is self._MISSING:
            return None
        if self._expires_at is not None and self._timer() >= self._expires_at:
            self._value = self._MISSING
            self._expires_at = None
            return None
        return self._value

    def set(self, value):
        self._value = value
        if self._seconds is None:
            self._expires_at = None
        else:
            self._expires_at = self._timer() + float(self._seconds)
