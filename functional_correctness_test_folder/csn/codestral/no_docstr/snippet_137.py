
class Reservoir:

    def __init__(self, traces_per_sec=0):
        self.traces_per_sec = traces_per_sec
        self.tokens = 0
        self.last_update_time = time.time()

    def take(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_update_time
        self.tokens += elapsed_time * self.traces_per_sec
        self.last_update_time = current_time

        if self.tokens >= 1:
            self.tokens -= 1
            return True
        else:
            return False
