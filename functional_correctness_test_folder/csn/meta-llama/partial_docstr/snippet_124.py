
import time


class DelayTimer:
    ''' Utility class that allows us to detect a certain
        time has passed'''

    def __init__(self, delay):
        self.delay = delay
        self.last_time = time.time()

    def is_time(self):
        current_time = time.time()
        if current_time - self.last_time >= self.delay:
            self.last_time = current_time
            return True
        return False

# Example usage:


def main():
    timer = DelayTimer(2)  # Create a timer with a 2-second delay
    while True:
        if timer.is_time():
            print("2 seconds have passed")
        # Simulate some work
        time.sleep(0.1)


if __name__ == "__main__":
    main()
