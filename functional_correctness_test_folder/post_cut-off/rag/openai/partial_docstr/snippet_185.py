
import heapq
from typing import List, Set, Dict, Tuple


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
        if m < 0:
            raise ValueError("m must be non‑negative")
        self.m: int = m
        self._counts: Dict[str, int] = {}
        self._heap: List[Tuple[int, str]] = []  # min‑heap of (count, string)
        self._heap_valid: bool = False  # indicates whether heap is up‑to‑date

    def add_strings(self, strings: List[str]) -> None:
        '''
        Add k strings to the data structure
        Args:
            strings: List of strings to add
        '''
        for s in strings:
            self._counts[s] = self._counts.get(s, 0) + 1
        self._heap_valid = False

    def add_string_dict(self, string_counts: dict) -> None:
        '''
        Add strings with their counts from a dictionary
        Args:
            string_counts: Dictionary mapping strings to their occurrence counts
        '''
        for s, c in string_counts.items():
            self._counts[s] = self._counts.get(s, 0) + c
        self._heap_valid = False

    def _cleanup_heap(self) -> None:
        '''
        Clean up outdated counts in heap and rebuild heap structure
        '''
        if self._heap_valid:
            return
        # Build a list of (count, string) for all items
        all_items = [(cnt, s) for s, cnt in self._counts.items()]
        # Keep only top m items
        if self.m == 0:
            self._heap = []
        else:
            # Use nlargest to get top m, then heapify to min‑heap
            top_m = heapq.nlargest(
                self.m, all_items, key=lambda x: (x[0], x[1]))
            # Convert to min‑heap
            self._heap = [(cnt, s) for cnt, s in top_m]
            heapq.heapify(self._heap)
        self._heap_valid = True

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
        # Use nlargest on the heap to get top k
        top_k = heapq.nlargest(k, self._heap, key=lambda x: (x[0], x[1]))
        return {s for _, s in top_k}

    def trim_to_m(self) -> None:
        '''
        Keep only the top-m strings by occurrence count, delete others
        '''
        if self.m == 0:
            self._counts.clear()
            self._heap = []
            self._heap_valid = True
            return
        self._cleanup_heap()
        # Keep only strings in the heap
        top_strings = {s for _, s in self._heap}
        # Remove others from counts
        for s in list(self._counts.keys()):
            if s not in top_strings:
                del self._counts[s]
        # After trimming, heap is already valid

    def size(self) -> int:
        '''Return the number of strings currently stored'''
        return len(self._counts)

    def get_count(self, string: str) -> int:
        '''Get the occurrence count of a specific string'''
        return self._counts.get(string, 0)
