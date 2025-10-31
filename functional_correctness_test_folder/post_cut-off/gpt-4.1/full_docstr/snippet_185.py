
from typing import List, Set
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
        self.counts = dict()  # string -> count
        self.heap = []        # min-heap of (count, string)
        self.heap_dirty = False

    def add_strings(self, strings: List[str]) -> None:
        '''
        Add k strings to the data structure
        Args:
            strings: List of strings to add
        '''
        for s in strings:
            self.counts[s] = self.counts.get(s, 0) + 1
        self.heap_dirty = True

    def add_string_dict(self, string_counts: dict) -> None:
        '''
        Add strings with their counts from a dictionary
        Args:
            string_counts: Dictionary mapping strings to their occurrence counts
        '''
        for s, c in string_counts.items():
            self.counts[s] = self.counts.get(s, 0) + c
        self.heap_dirty = True

    def _cleanup_heap(self) -> None:
        '''
        Clean up outdated counts in heap and rebuild heap structure
        '''
        # Build a heap of at most m items with largest counts
        if not self.heap_dirty:
            return
        self.heap = []
        for s, c in self.counts.items():
            if len(self.heap) < self.m:
                heapq.heappush(self.heap, (c, s))
            else:
                if c > self.heap[0][0]:
                    heapq.heappushpop(self.heap, (c, s))
        self.heap_dirty = False

    def get_top_k(self, k: int) -> Set[str]:
        '''
        Return the set of top-k strings by occurrence count
        Args:
            k: Number of strings to return
        Returns:
            Set containing the top-k strings
        '''
        if k <= 0 or not self.counts:
            return set()
        # Get top-k by count, break ties by string lex order
        # Use nlargest for efficiency
        items = heapq.nlargest(k, self.counts.items(),
                               key=lambda x: (x[1], x[0]))
        return set(s for s, c in items)

    def trim_to_m(self) -> None:
        '''
        Keep only the top-m strings by occurrence count, delete others
        '''
        if len(self.counts) <= self.m:
            return
        # Get top-m items
        items = heapq.nlargest(self.m, self.counts.items(),
                               key=lambda x: (x[1], x[0]))
        keep = set(s for s, c in items)
        # Remove others
        to_del = [s for s in self.counts if s not in keep]
        for s in to_del:
            del self.counts[s]
        self.heap_dirty = True

    def size(self) -> int:
        '''Return the number of strings currently stored'''
        return len(self.counts)

    def get_count(self, string: str) -> int:
        '''Get the occurrence count of a specific string'''
        return self.counts.get(string, 0)
