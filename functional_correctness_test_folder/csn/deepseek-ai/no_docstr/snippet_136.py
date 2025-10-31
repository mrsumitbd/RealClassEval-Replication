
import random
import time


class TraceId:

    def __init__(self):
        # Current time in milliseconds
        self.timestamp = int(time.time() * 1000)
        self.random_id = random.randint(0, 0xFFFF)  # 16-bit random number

    def to_id(self):
        return f"{self.timestamp:x}-{self.random_id:04x}"
