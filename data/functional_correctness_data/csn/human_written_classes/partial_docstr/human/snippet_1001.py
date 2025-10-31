import time

class ProcessInfo:
    """
    >>> p = ProcessInfo(100)
    >>> p.update(1)[0]
    99
    >>> p = ProcessInfo(100)
    >>> p.update(0)
    (100, '-', 0.0)
    """

    def __init__(self, total, use_last_rates=4):
        self.total = total
        self.use_last_rates = use_last_rates
        self.last_count = 0
        self.last_update = self.start_time = time.time()
        self.rate_info = []

    def update(self, count):
        current_duration = time.time() - self.last_update
        try:
            current_rate = float(count) / current_duration
            self.rate_info.append(current_rate)
            self.rate_info = self.rate_info[-self.use_last_rates:]
            smoothed_rate = sum(self.rate_info) / len(self.rate_info)
            rest = self.total - count
            eta = rest / smoothed_rate
        except ZeroDivisionError:
            return (self.total, '-', 0.0)
        human_eta = human_duration(eta)
        return (rest, human_eta, smoothed_rate)