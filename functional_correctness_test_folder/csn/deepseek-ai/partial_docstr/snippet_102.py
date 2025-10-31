
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
        if self.deadline is not None and self.timer() < self.deadline:
            return self.value
        return None

    def set(self, value):
        '''Sets the value and resets the deadline.'''
        self.value = value
        self.deadline = self.timer() + self.seconds
