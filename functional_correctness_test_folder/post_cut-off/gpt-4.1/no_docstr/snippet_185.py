
from typing import List, Set
import heapq


class TopKStringTracker:

    def __init__(self, m: int):
        self.m = m
        self.counts = dict()
        self.heap = []
        self.heap_dirty = False

    def add_strings(self, strings: List[str]) -> None:
        for s in strings:
            self.counts[s] = self.counts.get(s, 0) + 1
        self.heap_dirty = True

    def add_string_dict(self, string_counts: dict) -> None:
        for s, cnt in string_counts.items():
            self.counts[s] = self.counts.get(s, 0) + cnt
        self.heap_dirty = True

    def _cleanup_heap(self) -> None:
        if not self.heap_dirty:
            return
        self.heap = [(-cnt, s) for s, cnt in self.counts.items()]
        heapq.heapify(self.heap)
        self.heap_dirty = False

    def get_top_k(self, k: int) -> Set[str]:
        self._cleanup_heap()
        # Get k largest by count, then by string lex order
        items = sorted(self.counts.items(), key=lambda x: (-x[1], x[0]))
        return set([s for s, _ in items[:k]])

    def trim_to_m(self) -> None:
        if len(self.counts) <= self.m:
            return
        # Get top m by count, then by string lex order
        items = sorted(self.counts.items(), key=lambda x: (-x[1], x[0]))
        top_m = set([s for s, _ in items[:self.m]])
        # Remove others
        to_remove = [s for s in self.counts if s not in top_m]
        for s in to_remove:
            del self.counts[s]
        self.heap_dirty = True

    def size(self) -> int:
        return len(self.counts)

    def get_count(self, string: str) -> int:
        return self.counts.get(string, 0)
