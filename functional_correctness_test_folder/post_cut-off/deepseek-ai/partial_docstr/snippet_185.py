
import heapq
from typing import List, Set, Dict


class TopKStringTracker:
    def __init__(self, m: int):
        self.m = m
        self.counts: Dict[str, int] = {}
        self.heap: List[tuple] = []

    def add_strings(self, strings: List[str]) -> None:
        for s in strings:
            self.counts[s] = self.counts.get(s, 0) + 1

    def add_string_dict(self, string_counts: Dict[str, int]) -> None:
        for s, cnt in string_counts.items():
            self.counts[s] = self.counts.get(s, 0) + cnt

    def _cleanup_heap(self) -> None:
        new_heap = []
        for cnt, s in self.heap:
            if s in self.counts and self.counts[s] == cnt:
                heapq.heappush(new_heap, (cnt, s))
        self.heap = new_heap
        heapq.heapify(self.heap)

    def get_top_k(self, k: int) -> Set[str]:
        self._cleanup_heap()
        if k <= 0:
            return set()

        # If heap is not full, add all candidates
        if len(self.heap) < self.m:
            candidates = []
            for s, cnt in self.counts.items():
                if (cnt, s) not in self.heap:
                    candidates.append((cnt, s))
            for item in candidates:
                if len(self.heap) < self.m:
                    heapq.heappush(self.heap, item)
                else:
                    if item > self.heap[0]:
                        heapq.heappushpop(self.heap, item)

        # Now, heap contains min-heap of top m elements
        if not self.heap:
            return set()

        # Get top k from heap (k <= m)
        top_k = heapq.nlargest(k, self.heap)
        return {s for (cnt, s) in top_k}

    def trim_to_m(self) -> None:
        self._cleanup_heap()
        if len(self.heap) > self.m:
            new_heap = heapq.nlargest(self.m, self.heap)
            heapq.heapify(new_heap)
            self.heap = new_heap

    def size(self) -> int:
        return len(self.counts)

    def get_count(self, string: str) -> int:
        return self.counts.get(string, 0)
