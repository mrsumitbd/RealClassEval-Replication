
import time


class ExpiringCache:
    '''Simple cache with a deadline.'''

    def __init__(self, seconds, timer=time.time):
        '''C-tor.'''
        self._seconds = seconds
        self._timer = timer
        self._value = None
        self._expiry = None

    def get(self):
        '''Returns existing value, or None if deadline has expired.'''
        if self._value is None or self._expiry is None:
            return None
        if self._timer() > self._expiry:
            self._value = None
            self._expiry = None
            return None
        return self._value

    def set(self, value):
        self._value = value
        self._expiry = self._timer() + self._seconds
