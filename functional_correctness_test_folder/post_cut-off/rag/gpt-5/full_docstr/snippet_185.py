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
        if m < 0:
            raise ValueError("m must be non-negative")
        self.m: int = int(m)
        self._counts: Dict[str, int] = {}
        self._heap: List[tuple[int, str]] = []
        self._dirty: bool = True

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
            self._counts[s] = self._counts.get(s, 0) + 1
        self._dirty = True

    def add_string_dict(self, string_counts: dict) -> None:
        '''
        Add strings with their counts from a dictionary
        Args:
            string_counts: Dictionary mapping strings to their occurrence counts
        '''
        if not string_counts:
            return
        for s, c in string_counts.items():
            if s is None:
                continue
            try:
                inc = int(c)
            except Exception:
                continue
            if inc <= 0:
                continue
            self._counts[s] = self._counts.get(s, 0) + inc
        self._dirty = True

    def _cleanup_heap(self) -> None:
        '''
        Clean up outdated counts in heap and rebuild heap structure
        '''
        if self.m == 0 or not self._counts:
            self._heap = []
            self._dirty = False
            return
        new_heap: List[tuple[int, str]] = []
        limit = self.m
        for s, cnt in self._counts.items():
            item = (cnt, s)
            if len(new_heap) < limit:
                heapq.heappush(new_heap, item)
            else:
                if item > new_heap[0]:
                    heapq.heapreplace(new_heap, item)
        self._heap = new_heap
        self._dirty = False

    def get_top_k(self, k: int) -> Set[str]:
        '''
        Return the set of top-k strings by occurrence count
        Args:
            k: Number of strings to return
        Returns:
            Set containing the top-k strings
        '''
        if k <= 0 or not self._counts:
            return set()
        if self._dirty or len(self._heap) != min(self.m, len(self._counts)):
            self._cleanup_heap()
        if not self._heap:
            return set()
        top_n = min(k, len(self._heap))
        best = heapq.nlargest(top_n, self._heap, key=lambda t: (t[0], t[1]))
        return {s for _, s in best}

    def trim_to_m(self) -> None:
        '''
        Keep only the top-m strings by occurrence count, delete others
        '''
        if not self._counts or self.m <= 0:
            if self.m == 0:
                self._counts.clear()
                self._heap = []
                self._dirty = False
            return
        if self._dirty or len(self._heap) != min(self.m, len(self._counts)):
            self._cleanup_heap()
        keep = {s for _, s in self._heap}
        if len(keep) == len(self._counts):
            return
        to_delete = [s for s in self._counts.keys() if s not in keep]
        for s in to_delete:
            del self._counts[s]
        self._dirty = False
        # Rebuild heap to reflect trimmed counts precisely
        self._cleanup_heap()

    def size(self) -> int:
        '''Return the number of strings currently stored'''
        return len(self._counts)

    def get_count(self, string: str) -> int:
        '''Get the occurrence count of a specific string'''
        return self._counts.get(string, 0)
