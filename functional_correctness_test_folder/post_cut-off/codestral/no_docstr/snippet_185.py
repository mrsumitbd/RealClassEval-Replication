
import heapq
from typing import List, Set, Dict


class TopKStringTracker:

    def __init__(self, m: int):
        self.m = m
        self.string_counts = {}
        self.heap = []

    def add_strings(self, strings: List[str]) -> None:
        for string in strings:
            self.string_counts[string] = self.string_counts.get(string, 0) + 1
        self._cleanup_heap()

    def add_string_dict(self, string_counts: Dict[str, int]) -> None:
        for string, count in string_counts.items():
            self.string_counts[string] = self.string_counts.get(
                string, 0) + count
        self._cleanup_heap()

    def _cleanup_heap(self) -> None:
        self.heap = []
        for string, count in self.string_counts.items():
            heapq.heappush(self.heap, (count, string))
        while len(self.heap) > self.m:
            heapq.heappop(self.heap)

    def get_top_k(self, k: int) -> Set[str]:
        if k > len(self.heap):
            k = len(self.heap)
        top_k = set()
        temp_heap = self.heap.copy()
        for _ in range(k):
            count, string = heapq.heappop(temp_heap)
            top_k.add(string)
        return top_k

    def trim_to_m(self) -> None:
        self._cleanup_heap()

    def size(self) -> int:
        return len(self.string_counts)

    def get_count(self, string: str) -> int:
        return self.string_counts.get(string, 0)
