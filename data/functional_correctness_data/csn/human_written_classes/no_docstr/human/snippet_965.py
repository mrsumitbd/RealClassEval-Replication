from statistics import mean, stdev

class BodySize:

    def __init__(self, initial_limit):
        self.initial_limit = initial_limit
        self.collected_sizes = []
        self.calculated_limit = None

    @property
    def applicable_limit(self):
        return self.calculated_limit or self.initial_limit

    def add(self, length):
        if self.calculated_limit is None:
            self.collected_sizes.append(length)
            if len(self.collected_sizes) > 500:
                self.calculated_limit = int(mean(self.collected_sizes) + 5 * stdev(self.collected_sizes))
                logger.info('Updating max body size to %s', self.calculated_limit)