
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

    def add_string_dict(self, string_counts: dict) -> None:
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
        # Rebuild heap from current counts
        self.heap = [(cnt, s) for s, cnt in self.counts.items()]
        heapq.heapify(self.heap)

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
        # Ensure heap is up to date
        self._cleanup_heap()
        # If k >= number of distinct strings, return all
        if k >= len(self.counts):
            return set(self.counts.keys())
        # Get k largest by count
        largest = heapq.nlargest(k, self.heap)
        return {s for _, s in largest}

    def trim_to_m(self) -> None:
        '''
        Keep only the top-m strings in the data structure
        '''
        if self.m <= 0:
            # Remove all entries
            self.counts.clear()
            self.heap.clear()
            return
        # Ensure heap is up to date
        self._cleanup_heap()
        # Keep only top m
        top_m = heapq.nlargest(self.m, self.heap)
        # Rebuild counts dict to only these strings
        new_counts = {s: cnt for cnt, s in top_m}
        self.counts = new_counts
        # Rebuild heap accordingly
        self.heap = [(cnt, s) for s, cnt in new_counts.items()]
        heapq.heapify(self.heap)

    def size(self) -> int:
        '''Return the number of strings currently stored'''
        return len(self.counts)

    def get_count(self, string: str) -> int:
        '''Return the count of a specific string'''
        return self.counts.get(string, 0)
