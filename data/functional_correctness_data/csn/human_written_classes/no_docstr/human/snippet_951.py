import numpy as np

class BatchedRatingsIterator:

    def __init__(self, path, batch_size, total):
        self.ratings_iterable = RatingsIterable(path)
        self.batch_size = batch_size
        self.total = total

    def __len__(self):
        quotient, remainder = divmod(self.total, self.batch_size)
        return quotient + int(remainder != 0)

    def __iter__(self):
        i = 0
        iterable = iter(self.ratings_iterable)
        ratings = next(iterable)
        residual = None
        while True:
            if i + self.batch_size < len(ratings):
                if residual is None:
                    yield ratings[i:i + self.batch_size]
                    i += self.batch_size
                else:
                    delta = self.batch_size - len(residual)
                    yield np.concatenate([residual, ratings[:delta]], axis=0)
                    i += delta
                    residual = None
            else:
                residual = ratings[i:]
                i = 0
                try:
                    ratings = next(iterable)
                except StopIteration:
                    yield residual
                    break