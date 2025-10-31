
import heapq
from typing import List, Set, Dict


class TopKStringTracker:
    '''
    Efficient Top-K string tracking data structure
    Core ideas:
    1. Use hash table to record string counts
    2. Use min-heap to maintain top-m strings (heap root is the m-th largest element)
    3. Lazy cleanup: avoid frequent heap operations
    '''

    def __init__(self, m: int):
        self.m = m
        self.string_counts = {}
        self.min_heap = []
        self.lazy_removed = set()

    def add_strings(self, strings: List[str]) -> None:
        '''
        Add k strings to the data structure
        Args:
            strings: List of strings to add
        '''
        for s in strings:
            self.string_counts[s] = self.string_counts.get(s, 0) + 1
        self._lazy_update_heap(strings)

    def add_string_dict(self, string_counts: Dict[str, int]) -> None:
        '''
        Add strings with their counts from a dictionary
        Args:
            string_counts: Dictionary mapping strings to their occurrence counts
        '''
        for s, count in string_counts.items():
            self.string_counts[s] = self.string_counts.get(s, 0) + count
        self._lazy_update_heap(list(string_counts.keys()))

    def _lazy_update_heap(self, strings: List[str]) -> None:
        for s in strings:
            if s not in self.lazy_removed and (not self.min_heap or self.string_counts[s] > self.min_heap[0][0]):
                heapq.heappush(self.min_heap, (self.string_counts[s], s))
                if len(self.min_heap) > self.m:
                    _, removed = heapq.heappop(self.min_heap)
                    self.lazy_removed.add(removed)

    def _cleanup_heap(self) -> None:
        '''
        Clean up outdated counts in heap and rebuild heap structure
        '''
        self.min_heap = [(self.string_counts[s], s)
                         for _, s in self.min_heap if s not in self.lazy_removed]
        heapq.heapify(self.min_heap)
        self.lazy_removed = set()
        while len(self.min_heap) > self.m:
            _, removed = heapq.heappop(self.min_heap)
            self.lazy_removed.add(removed)

    def get_top_k(self, k: int) -> Set[str]:
        '''
        Return the set of top-k strings by occurrence count
        Args:
            k: Number of strings to return
        Returns:
            Set containing the top-k strings
        '''
        if len(self.min_heap) < self.m or k > len(self.min_heap):
            self._cleanup_heap()
        top_k = set([s for _, s in heapq.nlargest(k, self.min_heap)])
        return top_k

    def trim_to_m(self) -> None:
        self._cleanup_heap()

    def size(self) -> int:
        '''Return the number of strings currently stored'''
        return len(self.string_counts)

    def get_count(self, string: str) -> int:
        return self.string_counts.get(string, 0)
