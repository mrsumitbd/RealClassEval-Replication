
import heapq
from typing import List, Set, Dict


class TopKStringTracker:

    def __init__(self, m: int):
        self.m = m
        self.counts: Dict[str, int] = {}
        self.heap: List[tuple] = []

    def add_strings(self, strings: List[str]) -> None:
        for s in strings:
            if s in self.counts:
                self.counts[s] += 1
            else:
                self.counts[s] = 1
            heapq.heappush(self.heap, (self.counts[s], s))
        self._cleanup_heap()

    def add_string_dict(self, string_counts: Dict[str, int]) -> None:
        for s, cnt in string_counts.items():
            if s in self.counts:
                self.counts[s] += cnt
            else:
                self.counts[s] = cnt
            heapq.heappush(self.heap, (self.counts[s], s))
        self._cleanup_heap()

    def _cleanup_heap(self) -> None:
        while len(self.heap) > 0 and self.counts.get(self.heap[0][1], 0) != self.heap[0][0]:
            heapq.heappop(self.heap)

    def get_top_k(self, k: int) -> Set[str]:
        self._cleanup_heap()
        top_k = heapq.nlargest(k, self.heap)
        return {s for (cnt, s) in top_k}

    def trim_to_m(self) -> None:
        self._cleanup_heap()
        if len(self.counts) > self.m:
            to_remove = len(self.counts) - self.m
            for _ in range(to_remove):
                if self.heap:
                    _, s = heapq.heappop(self.heap)
                    if s in self.counts:
                        del self.counts[s]
            self._cleanup_heap()

    def size(self) -> int:
        return len(self.counts)

    def get_count(self, string: str) -> int:
        return self.counts.get(string, 0)
