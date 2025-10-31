
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
        self.heap_set = set()

    def add_strings(self, strings: List[str]) -> None:
        '''
        Add k strings to the data structure
        Args:
            strings: List of strings to add
        '''
        for s in strings:
            if s in self.counts:
                self.counts[s] += 1
            else:
                self.counts[s] = 1

    def add_string_dict(self, string_counts: dict) -> None:
        '''
        Add strings with their counts from a dictionary
        Args:
            string_counts: Dictionary mapping strings to their occurrence counts
        '''
        for s, cnt in string_counts.items():
            if s in self.counts:
                self.counts[s] += cnt
            else:
                self.counts[s] = cnt

    def _cleanup_heap(self) -> None:
        '''
        Clean up outdated counts in heap and rebuild heap structure
        '''
        new_heap = []
        new_heap_set = set()
        for cnt, s in self.heap:
            if s in self.counts and self.counts[s] == cnt:
                heapq.heappush(new_heap, (cnt, s))
                new_heap_set.add(s)
        self.heap = new_heap
        self.heap_set = new_heap_set

    def get_top_k(self, k: int) -> Set[str]:
        '''
        Return the set of top-k strings by occurrence count
        Args:
            k: Number of strings to return
        Returns:
            Set containing the top-k strings
        '''
        self._cleanup_heap()
        top_k = []
        for s, cnt in self.counts.items():
            if len(top_k) < k:
                heapq.heappush(top_k, (cnt, s))
            else:
                if cnt > top_k[0][0]:
                    heapq.heappop(top_k)
                    heapq.heappush(top_k, (cnt, s))
        return {s for (cnt, s) in top_k}

    def trim_to_m(self) -> None:
        '''
        Keep only the top-m strings by occurrence count, delete others
        '''
        self._cleanup_heap()
        top_m = self.get_top_k(self.m)
        keys = list(self.counts.keys())
        for s in keys:
            if s not in top_m:
                del self.counts[s]

    def size(self) -> int:
        '''Return the number of strings currently stored'''
        return len(self.counts)

    def get_count(self, string: str) -> int:
        '''Get the occurrence count of a specific string'''
        return self.counts.get(string, 0)
