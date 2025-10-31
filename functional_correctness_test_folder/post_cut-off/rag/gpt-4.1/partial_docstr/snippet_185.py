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
        '''
        Initialize the data structure
        Args:
            m: Maximum number of strings to retain
        '''
        self.m = m
        self.counts = {}  # str -> int
        self.heap = []    # list of (count, string)
        self.heap_set = set()  # set of strings currently in heap
        self.dirty = False

    def add_strings(self, strings: List[str]) -> None:
        '''
        Add k strings to the data structure
        Args:
            strings: List of strings to add
        '''
        for s in strings:
            self.counts[s] = self.counts.get(s, 0) + 1
        self.dirty = True

    def add_string_dict(self, string_counts: dict) -> None:
        '''
        Add strings with their counts from a dictionary
        Args:
            string_counts: Dictionary mapping strings to their occurrence counts
        '''
        for s, c in string_counts.items():
            self.counts[s] = self.counts.get(s, 0) + c
        self.dirty = True

    def _cleanup_heap(self) -> None:
        '''
        Clean up outdated counts in heap and rebuild heap structure
        '''
        # Rebuild heap from current counts, keep only top-m
        if not self.counts:
            self.heap = []
            self.heap_set = set()
            self.dirty = False
            return
        # Get top-m items by count (descending), then by string (for tie-breaking)
        items = [(-cnt, s) for s, cnt in self.counts.items()]
        # heapq.nlargest returns largest, so use -cnt for max-heap
        top_items = heapq.nsmallest(self.m, items)
        self.heap = [(-cnt, s) for cnt, s in top_items]
        heapq.heapify(self.heap)
        self.heap_set = set(s for _, s in self.heap)
        self.dirty = False

    def get_top_k(self, k: int) -> Set[str]:
        '''
        Return the set of top-k strings by occurrence count
        Args:
            k: Number of strings to return
        Returns:
            Set containing the top-k strings
        '''
        if self.dirty:
            self._cleanup_heap()
        # Get top-k from counts
        if not self.counts or k <= 0:
            return set()
        # Use heapq.nlargest for efficiency
        topk = heapq.nlargest(k, self.counts.items(),
                              key=lambda x: (x[1], x[0]))
        return set(s for s, _ in topk)

    def trim_to_m(self) -> None:
        '''
        Keep only the top-m strings by occurrence count, delete others
        '''
        if self.dirty:
            self._cleanup_heap()
        if not self.counts or len(self.counts) <= self.m:
            return
        # Get top-m keys
        topm = heapq.nlargest(self.m, self.counts.items(),
                              key=lambda x: (x[1], x[0]))
        topm_keys = set(s for s, _ in topm)
        # Remove all others
        to_del = [s for s in self.counts if s not in topm_keys]
        for s in to_del:
            del self.counts[s]
        self.dirty = True

    def size(self) -> int:
        '''Return the number of strings currently stored'''
        return len(self.counts)

    def get_count(self, string: str) -> int:
        '''Get the occurrence count of a specific string'''
        return self.counts.get(string, 0)
