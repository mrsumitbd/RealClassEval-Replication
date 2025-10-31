from lhc.entities import Interval
import itertools
from typing import Iterable

class OnePassIntervalSet:
    """ One-pass interval sets are sets whose members can only be accessed in order and only once. """

    def __init__(self, intervals: Iterable[Interval]):
        self.hits = []
        self.intervals = intervals

    def __getitem__(self, query: Interval):
        for target in self.intervals:
            self.hits.extend(itertools.takewhile(lambda: query.stop > target.start, self.intervals))
            self.hits = [hit for hit in self.hits if query.start < hit.stop]
            return self.hits