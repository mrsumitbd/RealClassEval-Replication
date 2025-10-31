
import time


class ExpiringCache:
    '''Simple cache with a deadline.'''

    def __init__(self, seconds, timer=time.time):
        '''C-tor.'''
        self._seconds = seconds
        self._timer = timer
        self._value = None
        self._expire_at = None

    def get(self):
        '''Returns existing value, or None if deadline has expired.'''
        if self._value is None or self._expire_at is None:
            return None
        if self._timer() >= self._expire_at:
            self._value = None
            self._expire_at = None
            return None
        return self._value

    def set(self, value):
        '''Set new value and reset the deadline for expiration.'''
        self._value = value
        self._expire_at = self._timer() + self._seconds
