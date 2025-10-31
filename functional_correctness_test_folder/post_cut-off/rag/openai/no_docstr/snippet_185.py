
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
        self.m = max(0, m)
        self.counts: Dict[str, int] = {}
        self.heap: List[tuple[int, str]] = []  # min-heap of (count, string)

    def add_strings(self, strings: List[str]) -> None:
        '''
        Add k strings to the data structure
        Args:
            strings: List of strings to add
        '''
        if not strings:
            return
        for s in strings:
            new_count = self.counts.get(s, 0) + 1
            self.counts[s] = new_count
            heapq.heappush(self.heap, (new_count, s))
        self._cleanup_heap()

    def add_string_dict(self, string_counts: dict) -> None:
        '''
        Add strings with their counts from a dictionary
        Args:
            string_counts: Dictionary mapping strings to their occurrence counts
        '''
        if not string_counts:
            return
        for s, c in string_counts.items():
            if c <= 0:
                continue
            new_count = self.counts.get(s, 0) + c
            self.counts[s] = new_count
            heapq.heappush(self.heap, (new_count, s))
        self._cleanup_heap()

    def _cleanup_heap(self) -> None:
        '''
        Clean up outdated counts in heap and rebuild heap structure
        '''
        # Remove stale entries
        while self.heap:
            count, s = self.heap[0]
            if self.counts.get(s, 0) != count:
                heapq.heappop(self.heap)
            else:
                break

        # Trim heap to size m
        if self.m <= 0:
            self.heap.clear()
            return

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
        if k <= 0:
            return set()
        self._cleanup_heap()
        # Use nlargest to get top k entries
        top_k = heapq.nlargest(k, self.heap, key=lambda x: (x[0], x[1]))
        return {s for _, s in top_k}

    def trim_to_m(self) -> None:
        '''
        Keep only the top-m strings by occurrence count, delete others
        '''
        if self.m <= 0:
            self.counts.clear()
            self.heap.clear()
            return

        self._cleanup_heap()
        top_m = self.get_top_k(self.m)
        # Filter counts dict
        self.counts = {s: self.counts[s] for s in top_m}
        # Rebuild heap
        self.heap = [(self.counts[s], s) for s in top_m]
        heapq.heapify(self.heap)

    def size(self) -> int:
        '''Return the number of strings currently stored'''
        return len(self.counts)

    def get_count(self, string: str) -> int:
        '''Get the occurrence count of a specific string'''
        return self.counts.get(string, 0)
