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
        self.m = max(0, int(m))
        self.counts: dict[str, int] = {}
        self._heap: list[tuple[int, str]] = []

    def add_strings(self, strings: List[str]) -> None:
        '''
        Add k strings to the data structure
        Args:
            strings: List of strings to add
        '''
        if not strings:
            return
        for s in strings:
            if s is None:
                continue
            c = self.counts.get(s, 0) + 1
            self.counts[s] = c
            if self.m == 0:
                continue
            if len(self._heap) < self.m:
                heapq.heappush(self._heap, (c, s))
            else:
                root_c, root_s = self._heap[0]
                if c > root_c or (c == root_c and s < root_s):
                    heapq.heappush(self._heap, (c, s))

    def add_string_dict(self, string_counts: dict) -> None:
        '''
        Add strings with their counts from a dictionary
        Args:
            string_counts: Dictionary mapping strings to their occurrence counts
        '''
        if not string_counts:
            return
        for s, v in string_counts.items():
            try:
                inc = int(v)
            except Exception:
                continue
            if inc <= 0 or s is None:
                continue
            c = self.counts.get(s, 0) + inc
            self.counts[s] = c
            if self.m == 0:
                continue
            if len(self._heap) < self.m:
                heapq.heappush(self._heap, (c, s))
            else:
                root_c, root_s = self._heap[0]
                if c > root_c or (c == root_c and s < root_s):
                    heapq.heappush(self._heap, (c, s))

    def _cleanup_heap(self) -> None:
        '''
        Clean up outdated counts in heap and rebuild heap structure
        '''
        if self.m == 0 or not self.counts:
            self._heap = []
            return
        # Select top-m by (count desc, string asc) for determinism
        items = self.counts.items()
        # Use nlargest to pick top-m efficiently
        top_m = heapq.nlargest(self.m, items, key=lambda kv: (kv[1], kv[0]))
        self._heap = [(cnt, s) for s, cnt in top_m]
        heapq.heapify(self._heap)

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
        # Clean to ensure accurate top view
        self._cleanup_heap()
        # If k is small, we can use the heap; otherwise use counts directly
        if k <= len(self._heap):
            top = heapq.nlargest(k, self._heap)
            return {s for _, s in top}
        # Fall back to counts for k > heap size
        top_items = heapq.nlargest(
            k, self.counts.items(), key=lambda kv: (kv[1], kv[0]))
        return {s for s, _ in top_items}

    def trim_to_m(self) -> None:
        '''
        Keep only the top-m strings by occurrence count, delete others
        '''
        if self.m <= 0 or not self.counts:
            self.counts.clear()
            self._heap = []
            return
        top_items = heapq.nlargest(
            self.m, self.counts.items(), key=lambda kv: (kv[1], kv[0]))
        # Rebuild counts dict with only top-m
        self.counts = {s: cnt for s, cnt in top_items}
        # Rebuild heap accordingly
        self._heap = [(cnt, s) for s, cnt in top_items]
        heapq.heapify(self._heap)

    def size(self) -> int:
        '''Return the number of strings currently stored'''
        return len(self.counts)

    def get_count(self, string: str) -> int:
        '''Get the occurrence count of a specific string'''
        return self.counts.get(string, 0)
