
from typing import List, Set, Dict
import heapq
import collections


class TopKStringTracker:

    def __init__(self, m: int):
        self.m = m
        self.counts = collections.Counter()
        self.heap = []

    def add_strings(self, strings: List[str]) -> None:
        for s in strings:
            self.counts[s] += 1
        self._cleanup_heap()

    def add_string_dict(self, string_counts: Dict[str, int]) -> None:
        for s, count in string_counts.items():
            self.counts[s] += count
        self._cleanup_heap()

    def _cleanup_heap(self) -> None:
        self.heap = [(-count, s) for s, count in self.counts.items()]
        heapq.heapify(self.heap)
        while len(self.heap) > self.m:
            heapq.heappop(self.heap)

    def get_top_k(self, k: int) -> Set[str]:
        return {s for _, s in heapq.nsmallest(min(k, len(self.heap)), self.heap)}

    def trim_to_m(self) -> None:
        self._cleanup_heap()

    def size(self) -> int:
        return len(self.heap)

    def get_count(self, string: str) -> int:
        return self.counts.get(string, 0)
