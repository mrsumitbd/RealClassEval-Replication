
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
        '''
        Initialize the data structure
        Args:
            m: Maximum number of strings to retain
        '''
        self.m = m
        self.counts = {}
        self.heap = []

    def add_strings(self, strings: List[str]) -> None:
        '''
        Add k strings to the data structure
        Args:
            strings: List of strings to add
        '''
        for s in strings:
            self.counts[s] = self.counts.get(s, 0) + 1
            heapq.heappush(self.heap, (self.counts[s], s))

    def add_string_dict(self, string_counts: dict) -> None:
        '''
        Add strings with their counts from a dictionary
        Args:
            string_counts: Dictionary mapping strings to their occurrence counts
        '''
        for s, count in string_counts.items():
            self.counts[s] = self.counts.get(s, 0) + count
            heapq.heappush(self.heap, (self.counts[s], s))

    def _cleanup_heap(self) -> None:
        '''
        Clean up outdated counts in heap and rebuild heap structure
        '''
        new_heap = []
        for count, s in self.heap:
            if self.counts.get(s, 0) == count:
                heapq.heappush(new_heap, (count, s))
        self.heap = new_heap

    def get_top_k(self, k: int) -> Set[str]:
        '''
        Return the set of top-k strings by occurrence count
        Args:
            k: Number of strings to return
        Returns:
            Set containing the top-k strings
        '''
        if k > self.m:
            k = self.m
        self._cleanup_heap()
        top_k = set()
        temp_heap = self.heap.copy()
        for _ in range(min(k, len(temp_heap))):
            count, s = heapq.heappop(temp_heap)
            top_k.add(s)
        return top_k

    def trim_to_m(self) -> None:
        '''
        Keep only the top-m strings by occurrence count, delete others
        '''
        self._cleanup_heap()
        if len(self.heap) > self.m:
            new_heap = []
            for _ in range(self.m):
                new_heap.append(heapq.heappop(self.heap))
            self.heap = new_heap
            self.counts = {s: count for count, s in self.heap}

    def size(self) -> int:
        '''Return the number of strings currently stored'''
        return len(self.counts)

    def get_count(self, string: str) -> int:
        '''Get the occurrence count of a specific string'''
        return self.counts.get(string, 0)
