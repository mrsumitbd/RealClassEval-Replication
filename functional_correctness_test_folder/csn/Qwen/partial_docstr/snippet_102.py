
import time


class ExpiringCache:
    '''Simple cache with a deadline.'''

    def __init__(self, seconds, timer=time.time):
        '''C-tor.'''
        self.seconds = seconds
        self.timer = timer
        self.value = None
        self.expiry = None

    def get(self):
        '''Returns existing value, or None if deadline has expired.'''
        if self.expiry is not None and self.timer() < self.expiry:
            return self.value
        return None

    def set(self, value):
        self.value = value
        self.expiry = self.timer() + self.seconds
