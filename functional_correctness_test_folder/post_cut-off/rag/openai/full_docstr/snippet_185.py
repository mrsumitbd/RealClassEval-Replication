
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
        self.m = max(0, int(m))
        self.counts: Dict[str, int] = {}
        self.heap: List[tuple[int, str]] = []

    def add_strings(self, strings: List[str]) -> None:
        '''
        Add k strings to the data structure
        Args:
            strings: List of strings to add
        '''
        for s in strings:
            self.counts[s] = self.counts.get(s, 0) + 1
        self._cleanup_heap()

    def add_string_dict(self, string_counts: dict) -> None:
        '''
        Add strings with their counts from a dictionary
        Args:
            string_counts: Dictionary mapping strings to their occurrence counts
        '''
        for s, c in string_counts.items():
            self.counts[s] = self.counts.get(s, 0) + int(c)
        self._cleanup_heap()

    def _cleanup_heap(self) -> None:
        '''
        Clean up outdated counts in heap and rebuild heap structure
        '''
        # Build a heap of all current counts
        heap = [(cnt, s) for s, cnt in self.counts.items()]
        heapq.heapify(heap)
        # Keep only the largest m elements
        if self.m > 0:
            while len(heap) > self.m:
                heapq.heappop(heap)
        self.heap = heap

    def get_top_k(self, k: int) -> Set[str]:
        '''
        Return the set of top-k strings by occurrence count
        Args:
            k: Number of strings to return
        Returns:
            Set containing the top-k strings
        '''
        k = max(0, int(k))
        if k == 0:
            return set()

        # Use a copy of the heap to avoid modifying the original
        temp_heap = list(self.heap)
        heapq.heapify(temp_heap)

        result: Set[str] = set()
        seen: Set[str] = set()

        while temp_heap and len(result) < k:
            cnt, s = heapq.heappop(temp_heap)
            # Verify that the popped count matches the current count
            if self.counts.get(s, 0) == cnt and s not in seen:
                result.add(s)
                seen.add(s)

        # If we didn't get enough due to stale entries, fall back to full sort
        if len(result) < k:
            # Sort all items by count descending
            sorted_items = sorted(self.counts.items(),
                                  key=lambda x: (-x[1], x[0]))
            for s, _ in sorted_items[:k]:
                result.add(s)

        return result

    def trim_to_m(self) -> None:
        '''
        Keep only the top-m strings by occurrence count, delete others
        '''
        if self.m <= 0:
            self.counts.clear()
            self.heap.clear()
            return

        top_m = self.get_top_k(self.m)
        new_counts = {s: self.counts[s] for s in top_m}
        self.counts = new_counts
        self._cleanup_heap()

    def size(self) -> int:
        '''Return the number of strings currently stored'''
        return len(self.counts)

    def get_count(self, string: str) -> int:
        '''Get the occurrence count of a specific string'''
        return self.counts.get(string, 0)
