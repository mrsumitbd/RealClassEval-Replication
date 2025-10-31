
import time


class ExpiringCache:
    '''Simple cache with a deadline.'''

    def __init__(self, seconds, timer=time.time):
        '''C-tor.'''
        self.seconds = seconds
        self.timer = timer
        self.value = None
        self.deadline = None

    def get(self):
        '''Returns existing value, or None if deadline has expired.'''
        if self.deadline is None or self.timer() > self.deadline:
            return None
        return self.value

    def set(self, value):
        self.value = value
        self.deadline = self.timer() + self.seconds
