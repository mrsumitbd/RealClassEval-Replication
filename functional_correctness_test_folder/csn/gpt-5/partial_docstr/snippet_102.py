import time


class ExpiringCache:
    '''Simple cache with a deadline.'''

    def __init__(self, seconds, timer=time.time):
        '''C-tor.'''
        self._seconds = float(seconds)
        self._timer = timer
        self._value = None
        self._deadline = None

    def get(self):
        '''Returns existing value, or None if deadline has expired.'''
        if self._value is None or self._deadline is None:
            return None
        if self._timer() <= self._deadline:
            return self._value
        # Expired
        self._value = None
        self._deadline = None
        return None

    def set(self, value):
        self._value = value
        self._deadline = self._timer() + self._seconds
