
import heapq
from typing import List, Set, Dict


class TopKStringTracker:
    def __init__(self, m: int):
        self.m = m
        self.counts: Dict[str, int] = {}
        self.heap: List[tuple] = []
        self.heap_set: Set[str] = set()

    def add_strings(self, strings: List[str]) -> None:
        for s in strings:
            if s in self.counts:
                self.counts[s] += 1
            else:
                self.counts[s] = 1
            if s in self.heap_set:
                heapq.heapify(self.heap)  # Force heap rebuild if needed

    def add_string_dict(self, string_counts: Dict[str, int]) -> None:
        for s, cnt in string_counts.items():
            if s in self.counts:
                self.counts[s] += cnt
            else:
                self.counts[s] = cnt
            if s in self.heap_set:
                heapq.heapify(self.heap)  # Force heap rebuild if needed

    def _cleanup_heap(self) -> None:
        new_heap = []
        new_heap_set = set()
        for cnt, s in self.heap:
            if s in self.counts and self.counts[s] == cnt:
                heapq.heappush(new_heap, (cnt, s))
                new_heap_set.add(s)
        self.heap = new_heap
        self.heap_set = new_heap_set

    def get_top_k(self, k: int) -> Set[str]:
        self._cleanup_heap()
        if k <= 0:
            return set()

        # If heap is not full, populate it with all strings
        if len(self.heap) < self.m and len(self.counts) > len(self.heap):
            for s, cnt in self.counts.items():
                if s not in self.heap_set:
                    if len(self.heap) < self.m:
                        heapq.heappush(self.heap, (cnt, s))
                        self.heap_set.add(s)
                    else:
                        if cnt > self.heap[0][0]:
                            removed = heapq.heappop(self.heap)
                            self.heap_set.remove(removed[1])
                            heapq.heappush(self.heap, (cnt, s))
                            self.heap_set.add(s)

        # Now, extract top-k
        if len(self.heap) == 0:
            return set()

        # Use a max-heap approach by inverting counts
        temp_heap = []
        for cnt, s in self.heap:
            heapq.heappush(temp_heap, (-cnt, s))

        top_k = set()
        for _ in range(min(k, len(temp_heap))):
            neg_cnt, s = heapq.heappop(temp_heap)
            top_k.add(s)
        return top_k

    def trim_to_m(self) -> None:
        self._cleanup_heap()
        if len(self.heap) > self.m:
            new_heap = []
            new_heap_set = set()
            # Keep only top-m elements
            temp_heap = []
            for cnt, s in self.heap:
                heapq.heappush(temp_heap, (-cnt, s))
            for _ in range(self.m):
                neg_cnt, s = heapq.heappop(temp_heap)
                heapq.heappush(new_heap, (-neg_cnt, s))
                new_heap_set.add(s)
            self.heap = new_heap
            self.heap_set = new_heap_set

        # Remove strings not in heap from counts
        to_remove = []
        for s in self.counts:
            if s not in self.heap_set:
                to_remove.append(s)
        for s in to_remove:
            del self.counts[s]

    def size(self) -> int:
        return len(self.counts)

    def get_count(self, string: str) -> int:
        return self.counts.get(string, 0)
