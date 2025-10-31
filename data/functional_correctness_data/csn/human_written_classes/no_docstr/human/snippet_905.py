import time

class LongIterable:

    def __init__(self, duration=20):
        self.duration = duration
        n = 1000
        start = time.perf_counter()

        def test_iter():
            for index in range(n):
                yield index
        for _ in test_iter():
            pass
        stop = time.perf_counter()
        stop = time.perf_counter()
        time_per_iter = (stop - start) / n * 5
        num_iters = int(self.duration / time_per_iter)
        self.num_iters = num_iters

    def __len__(self):
        return self.num_iters

    def __iter__(self):
        for index in range(self.num_iters):
            yield index