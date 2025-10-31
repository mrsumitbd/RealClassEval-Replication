
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
        self.string_counts = {}
        self.min_heap = []
        self.lazy_removed = set()

    def add_strings(self, strings: List[str]) -> None:
        '''
        Add k strings to the data structure
        Args:
            strings: List of strings to add
        '''
        for string in strings:
            self.string_counts[string] = self.string_counts.get(string, 0) + 1
            if string not in self.lazy_removed and (not self.min_heap or (string not in [x[1] for x in self.min_heap] and len(self.min_heap) < self.m or (string in [x[1] for x in self.min_heap]))):
                heapq.heappush(
                    self.min_heap, (self.string_counts[string], string))
                if len(self.min_heap) > self.m:
                    count, string = heapq.heappop(self.min_heap)
                    self.lazy_removed.add(string)

    def add_string_dict(self, string_counts: Dict[str, int]) -> None:
        '''
        Add strings with their counts from a dictionary
        Args:
            string_counts: Dictionary mapping strings to their occurrence counts
        '''
        for string, count in string_counts.items():
            self.string_counts[string] = self.string_counts.get(
                string, 0) + count
            if string not in self.lazy_removed and (not self.min_heap or (string not in [x[1] for x in self.min_heap] and len(self.min_heap) < self.m or (string in [x[1] for x in self.min_heap]))):
                heapq.heappush(
                    self.min_heap, (self.string_counts[string], string))
                if len(self.min_heap) > self.m:
                    count, string = heapq.heappop(self.min_heap)
                    self.lazy_removed.add(string)

    def _cleanup_heap(self) -> None:
        '''
        Clean up outdated counts in heap and rebuild heap structure
        '''
        self.min_heap = [(self.string_counts[string], string)
                         for count, string in self.min_heap if string not in self.lazy_removed]
        heapq.heapify(self.min_heap)
        self.lazy_removed = set()
        while len(self.min_heap) > self.m:
            count, string = heapq.heappop(self.min_heap)
            self.lazy_removed.add(string)

    def get_top_k(self, k: int) -> Set[str]:
        '''
        Return the set of top-k strings by occurrence count
        Args:
            k: Number of strings to return
        Returns:
            Set containing the top-k strings
        '''
        self._cleanup_heap()
        top_k = heapq.nlargest(k, self.min_heap)
        return set([string for count, string in top_k])

    def trim_to_m(self) -> None:
        '''
        Keep only the top-m strings by occurrence count, delete others
        '''
        self._cleanup_heap()
        top_m = set([string for count, string in self.min_heap])
        self.string_counts = {string: count for string,
                              count in self.string_counts.items() if string in top_m}

    def size(self) -> int:
        '''Return the number of strings currently stored'''
        return len(self.string_counts)

    def get_count(self, string: str) -> int:
        '''Get the occurrence count of a specific string'''
        return self.string_counts.get(string, 0)
