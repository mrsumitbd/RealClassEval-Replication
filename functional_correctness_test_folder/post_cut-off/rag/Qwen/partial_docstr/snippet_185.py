
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
        for string in strings:
            if string in self.counts:
                self.counts[string] += 1
            else:
                self.counts[string] = 1
            if len(self.heap) < self.m:
                heapq.heappush(self.heap, (self.counts[string], string))
            elif self.counts[string] > self.heap[0][0]:
                heapq.heapreplace(self.heap, (self.counts[string], string))

    def add_string_dict(self, string_counts: dict) -> None:
        '''
        Add strings with their counts from a dictionary
        Args:
            string_counts: Dictionary mapping strings to their occurrence counts
        '''
        for string, count in string_counts.items():
            if string in self.counts:
                self.counts[string] += count
            else:
                self.counts[string] = count
            if len(self.heap) < self.m:
                heapq.heappush(self.heap, (self.counts[string], string))
            elif self.counts[string] > self.heap[0][0]:
                heapq.heapreplace(self.heap, (self.counts[string], string))

    def _cleanup_heap(self) -> None:
        '''
        Clean up outdated counts in heap and rebuild heap structure
        '''
        self.heap = [(count, string)
                     for string, count in self.counts.items() if count > 0]
        heapq.heapify(self.heap)
        while len(self.heap) > self.m:
            heapq.heappop(self.heap)

    def get_top_k(self, k: int) -> Set[str]:
        '''
        Return the set of top-k strings by occurrence count
        Args:
            k: Number of strings to return
        Returns:
            Set containing the top-k strings
        '''
        self._cleanup_heap()
        return {string for count, string in heapq.nlargest(k, self.heap)}

    def trim_to_m(self) -> None:
        '''
        Keep only the top-m strings by occurrence count, delete others
        '''
        self._cleanup_heap()
        self.counts = {string: count for count, string in self.heap}
        self.heap = [(count, string) for count, string in self.heap]

    def size(self) -> int:
        '''Return the number of strings currently stored'''
        return len(self.counts)

    def get_count(self, string: str) -> int:
        '''Get the occurrence count of a specific string'''
        return self.counts.get(string, 0)
