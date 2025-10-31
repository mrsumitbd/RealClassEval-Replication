from typing import List, Set, Dict, Tuple
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
        self.m = int(m)
        self.counts: Dict[str, int] = {}
        self.heap: List[Tuple[int, str]] = []

    def add_strings(self, strings: List[str]) -> None:
        '''
        Add k strings to the data structure
        Args:
            strings: List of strings to add
        '''
        if not strings:
            return
        local: Dict[str, int] = {}
        for s in strings:
            if s is None:
                continue
            local[s] = local.get(s, 0) + 1
        for s, c in local.items():
            self.counts[s] = self.counts.get(s, 0) + c
        self.trim_to_m()

    def add_string_dict(self, string_counts: dict) -> None:
        '''
        Add strings with their counts from a dictionary
        Args:
            string_counts: Dictionary mapping strings to their occurrence counts
        '''
        if not string_counts:
            return
        for s, c in string_counts.items():
            if c is None:
                continue
            if c <= 0:
                continue
            if s is None:
                continue
            self.counts[s] = self.counts.get(s, 0) + int(c)
        self.trim_to_m()

    def _cleanup_heap(self) -> None:
        '''
        Clean up outdated counts in heap and rebuild heap structure
        '''
        if self.m <= 0 or not self.counts:
            self.heap = []
            return
        # Build top-m entries from current counts
        # Use nlargest to select top m by count (and string for tie-break determinism)
        top = heapq.nlargest(self.m, self.counts.items(),
                             key=lambda kv: (kv[1], kv[0]))
        self.heap = [(cnt, s) for s, cnt in top]
        heapq.heapify(self.heap)

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
        if k <= self.m and self.m > 0:
            self._cleanup_heap()
            # Sort heap entries by descending count, then string for stability
            ordered = sorted(self.heap, key=lambda x: (-x[0], x[1]))
            return {s for _, s in ordered[:k]}
        # If k exceeds maintained m, compute directly from counts
        topk = heapq.nlargest(k, self.counts.items(),
                              key=lambda kv: (kv[1], kv[0]))
        return {s for s, _ in topk}

    def trim_to_m(self) -> None:
        self._cleanup_heap()

    def size(self) -> int:
        '''Return the number of strings currently stored'''
        return len(self.counts)

    def get_count(self, string: str) -> int:
        return self.counts.get(string, 0)
