
import time


class ExpiringCache:
    '''Simple cache with a deadline.'''

    def __init__(self, seconds, timer=time.time):
        '''C-tor.'''
        self.seconds = seconds
        self.timer = timer
        self.deadline = None
        self.value = None

    def get(self):
        '''Returns existing value, or None if deadline has expired.'''
        if self.deadline is None or self.timer() > self.deadline:
            return None
        return self.value

    def set(self, value):
        '''Sets the value and updates the deadline.'''
        self.value = value
        self.deadline = self.timer() + self.seconds

# Example usage:


def main():
    cache = ExpiringCache(5)  # 5 seconds expiration
    cache.set("Hello, World!")
    print(cache.get())  # Should print: Hello, World!
    time.sleep(6)
    print(cache.get())  # Should print: None


if __name__ == "__main__":
    main()
