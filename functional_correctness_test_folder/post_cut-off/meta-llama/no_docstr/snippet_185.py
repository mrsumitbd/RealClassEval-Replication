
import heapq
from typing import List, Set, Dict


class TopKStringTracker:

    def __init__(self, m: int):
        self.m = m
        self.string_counts = {}
        self.min_heap = []

    def add_strings(self, strings: List[str]) -> None:
        for string in strings:
            self.string_counts[string] = self.string_counts.get(string, 0) + 1
            self._push_to_heap(string)

    def add_string_dict(self, string_counts: Dict[str, int]) -> None:
        for string, count in string_counts.items():
            self.string_counts[string] = self.string_counts.get(
                string, 0) + count
            self._push_to_heap(string)

    def _push_to_heap(self, string: str) -> None:
        if len(self.min_heap) < self.m:
            heapq.heappush(self.min_heap, (self.string_counts[string], string))
        elif self.string_counts[string] > self.min_heap[0][0]:
            heapq.heappop(self.min_heap)
            heapq.heappush(self.min_heap, (self.string_counts[string], string))
        self._cleanup_heap()

    def _cleanup_heap(self) -> None:
        while self.min_heap and self.min_heap[0][0] != self.string_counts[self.min_heap[0][1]]:
            heapq.heappop(self.min_heap)

    def get_top_k(self, k: int) -> Set[str]:
        top_k = set([string for _, string in heapq.nlargest(k, self.min_heap)])
        top_k.update([string for string, count in self.string_counts.items(
        ) if count > self.min_heap[0][0]])
        return set(list(top_k)[:k])

    def trim_to_m(self) -> None:
        self.min_heap = heapq.nlargest(self.m, self.min_heap)
        heapq.heapify(self.min_heap)

    def size(self) -> int:
        return len(self.string_counts)

    def get_count(self, string: str) -> int:
        return self.string_counts.get(string, 0)
