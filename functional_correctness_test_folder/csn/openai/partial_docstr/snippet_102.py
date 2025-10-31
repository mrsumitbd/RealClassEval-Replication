
import time


class ExpiringCache:
    '''Simple cache with a deadline.'''

    def __init__(self, seconds, timer=time.time):
        '''C-tor.'''
        self._seconds = seconds
        self._timer = timer
        self._value = None
        self._expires = None

    def get(self):
        '''Returns existing value, or None if deadline has expired.'''
        if self._expires is None:
            return None
        if self._timer() >= self._expires:
            self._value = None
            self._expires = None
            return None
        return self._value

    def set(self, value):
        '''Store value and set expiration deadline.'''
        self._value = value
        self._expires = self._timer() + self._seconds
