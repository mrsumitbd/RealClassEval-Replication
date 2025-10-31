import time


class ExpiringCache:
    '''Simple cache with a deadline.'''

    def __init__(self, seconds, timer=time.time):
        '''C-tor.'''
        self.seconds = float(seconds)
        self.timer = timer
        self._value = None
        self._deadline = None

    def get(self):
        '''Returns existing value, or None if deadline has expired.'''
        if self._deadline is None:
            return None
        if self.timer() >= self._deadline:
            self._value = None
            self._deadline = None
            return None
        return self._value

    def set(self, value):
        '''Set new value and reset the deadline for expiration.'''
        self._value = value
        self._deadline = self.timer() + self.seconds
