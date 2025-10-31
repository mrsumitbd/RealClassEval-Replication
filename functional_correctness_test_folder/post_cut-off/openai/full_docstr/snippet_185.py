
from typing import List, Set, Dict
import heapq


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
        self.counts: Dict[str, int] = {}
        self.heap: List[tuple[int, str]] = []  # min-heap of (count, string)

    def add_strings(self, strings: List[str]) -> None:
        '''
        Add k strings to the data structure
        Args:
            strings: List of strings to add
        '''
        for s in strings:
            new_count = self.counts.get(s, 0) + 1
            self.counts[s] = new_count
            heapq.heappush(self.heap, (new_count, s))

    def add_string_dict(self, string_counts: Dict[str, int]) -> None:
        '''
        Add strings with their counts from a dictionary
        Args:
            string_counts: Dictionary mapping strings to their occurrence counts
        '''
        for s, c in string_counts.items():
            new_count = self.counts.get(s, 0) + c
            self.counts[s] = new_count
            heapq.heappush(self.heap, (new_count, s))

    def _cleanup_heap(self) -> None:
        '''
        Clean up outdated counts in heap and rebuild heap structure
        '''
        # Rebuild heap from current counts, keeping only top-m
        if not self.counts:
            self.heap = []
            return
        top_m = heapq.nlargest(self.m, self.counts.items(), key=lambda x: x[1])
        self.heap = [(cnt, s) for s, cnt in top_m]
        heapq.heapify(self.heap)

    def get_top_k(self, k: int) -> Set[str]:
        '''
        Return the set of top-k strings by occurrence count
        Args:
            k: Number of strings to return
        Returns:
            Set containing the top-k strings
        '''
        if not self.counts:
            return set()
        top_k = heapq.nlargest(k, self.counts.items(), key=lambda x: x[1])
        return {s for s, _ in top_k}

    def trim_to_m(self) -> None:
        '''
        Keep only the top-m strings by occurrence count, delete others
        '''
        if not self.counts:
            return
        top_m = heapq.nlargest(self.m, self.counts.items(), key=lambda x: x[1])
        new_counts = {s: cnt for s, cnt in top_m}
        self.counts = new_counts
        self._cleanup_heap()

    def size(self) -> int:
        '''Return the number of strings currently stored'''
        return len(self.counts)

    def get_count(self, string: str) -> int:
        '''Get the occurrence count of a specific string'''
        return self.counts.get(string, 0)
