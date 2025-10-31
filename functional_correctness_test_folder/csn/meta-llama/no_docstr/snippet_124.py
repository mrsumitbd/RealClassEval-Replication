
import time


class DelayTimer:

    def __init__(self, delay):
        self.delay = delay
        self.start_time = time.time()

    def is_time(self):
        return time.time() - self.start_time >= self.delay

# Example usage:


def main():
    timer = DelayTimer(5)  # Create a timer with a 5-second delay
    while True:
        if timer.is_time():
            print("Time's up!")
            break
        print("Waiting...", end='\r')
        time.sleep(1)


if __name__ == "__main__":
    main()
