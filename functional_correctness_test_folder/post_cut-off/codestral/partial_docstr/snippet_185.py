
import heapq
from typing import List, Set


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
        self.heap = []

    def add_strings(self, strings: List[str]) -> None:
        '''
        Add k strings to the data structure
        Args:
            strings: List of strings to add
        '''
        for string in strings:
            self.string_counts[string] = self.string_counts.get(string, 0) + 1

    def add_string_dict(self, string_counts: dict) -> None:
        '''
        Add strings with their counts from a dictionary
        Args:
            string_counts: Dictionary mapping strings to their occurrence counts
        '''
        for string, count in string_counts.items():
            self.string_counts[string] = self.string_counts.get(
                string, 0) + count

    def _cleanup_heap(self) -> None:
        '''
        Clean up outdated counts in heap and rebuild heap structure
        '''
        new_heap = []
        for string, count in self.heap:
            if self.string_counts.get(string, 0) == count:
                heapq.heappush(new_heap, (count, string))
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
        for _ in range(k):
            if not temp_heap:
                break
            count, string = heapq.heappop(temp_heap)
            top_k.add(string)
        return top_k

    def trim_to_m(self) -> None:
        self._cleanup_heap()
        if len(self.heap) > self.m:
            self.heap = heapq.nsmallest(self.m, self.heap)

    def size(self) -> int:
        '''Return the number of strings currently stored'''
        return len(self.string_counts)

    def get_count(self, string: str) -> int:
        return self.string_counts.get(string, 0)
