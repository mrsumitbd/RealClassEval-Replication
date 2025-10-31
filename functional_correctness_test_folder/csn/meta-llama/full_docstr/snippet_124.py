
import time


class DelayTimer:
    ''' Utility class that allows us to detect a certain
        time has passed'''

    def __init__(self, delay):
        ''' Initialise the time with delay of dt seconds
        Parameters
        ----------
        delay: float
            The number of seconds in the timer
        '''
        self.delay = delay
        self.last_time = time.time()

    def is_time(self):
        '''
        Returns true if more than self.dt seconds has passed
        since the initialization or last call of successful is_time()
        Returns
        -------
        ret: bool
             True if specified amout of time has passed since the
             initialization or last successful is_time() call
        '''
        current_time = time.time()
        if current_time - self.last_time >= self.delay:
            self.last_time = current_time
            return True
        return False

# Example usage:


def main():
    timer = DelayTimer(2)  # Create a timer with 2 seconds delay
    while True:
        if timer.is_time():
            print("2 seconds have passed")
        # Simulating some work
        time.sleep(0.1)


if __name__ == "__main__":
    main()
