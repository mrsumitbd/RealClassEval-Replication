from typing import List, Set, Dict
import heapq
from collections import Counter


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
        if m <= 0:
            raise ValueError("m must be a positive integer")
        self.m: int = int(m)
        self.counts: Dict[str, int] = {}
        self.heap: List[tuple] = []
        self._heap_valid: bool = False

    def add_strings(self, strings: List[str]) -> None:
        '''
        Add k strings to the data structure
        Args:
            strings: List of strings to add
        '''
        if not strings:
            return
        tally = Counter(strings)
        for s, cnt in tally.items():
            if cnt <= 0:
                continue
            self.counts[s] = self.counts.get(s, 0) + cnt
        self._heap_valid = False

    def add_string_dict(self, string_counts: dict) -> None:
        '''
        Add strings with their counts from a dictionary
        Args:
            string_counts: Dictionary mapping strings to their occurrence counts
        '''
        if not string_counts:
            return
        for s, cnt in string_counts.items():
            if cnt is None or cnt <= 0:
                continue
            self.counts[s] = self.counts.get(s, 0) + int(cnt)
        self._heap_valid = False

    def _cleanup_heap(self) -> None:
        '''
        Clean up outdated counts in heap and rebuild heap structure
        '''
        if self._heap_valid:
            return
        h: List[tuple] = []
        # Maintain a min-heap of size up to m with (count, string)
        for s, c in self.counts.items():
            if c <= 0:
                continue
            if len(h) < self.m:
                heapq.heappush(h, (c, s))
            else:
                if c > h[0][0]:
                    heapq.heapreplace(h, (c, s))
        self.heap = h
        self._heap_valid = True

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
        self._cleanup_heap()
        total = len(self.counts)
        k_eff = min(k, total)
        if k_eff <= len(self.heap):
            # Use heap of top-m to derive top-k
            topk = heapq.nlargest(k_eff, self.heap)  # list of (count, string)
            return {s for _, s in topk}
        else:
            # Need more than m; compute from counts
            topk_items = heapq.nlargest(
                k_eff, self.counts.items(), key=lambda it: it[1])
            return {s for s, _ in topk_items}

    def trim_to_m(self) -> None:
        '''
        Keep only the top-m strings by occurrence count, delete others
        '''
        if not self.counts:
            self.heap = []
            self._heap_valid = True
            return
        self._cleanup_heap()
        keep = {s for _, s in self.heap}
        if len(keep) == len(self.counts):
            return
        self.counts = {s: self.counts[s] for s in keep}
        # Rebuild heap from trimmed counts
        self._heap_valid = False
        self._cleanup_heap()

    def size(self) -> int:
        '''Return the number of strings currently stored'''
        return len(self.counts)

    def get_count(self, string: str) -> int:
        '''Get the occurrence count of a specific string'''
        return self.counts.get(string, 0)
