from typing import List, Set, Dict, Optional, Tuple
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
        if m < 0:
            raise ValueError("m must be non-negative")
        self.m = m
        self._counts: Dict[str, int] = {}
        self._heap: List[Tuple[int, int, str]] = []  # (count, seq, string)
        # string -> count currently represented in heap
        self._in_heap_count: Dict[str, int] = {}
        self._seq: int = 0

    def add_strings(self, strings: List[str]) -> None:
        '''
        Add k strings to the data structure
        Args:
            strings: List of strings to add
        '''
        for s in strings:
            self._counts[s] = self._counts.get(s, 0) + 1
            self._consider_for_heap(s)

    def add_string_dict(self, string_counts: dict) -> None:
        '''
        Add strings with their counts from a dictionary
        Args:
            string_counts: Dictionary mapping strings to their occurrence counts
        '''
        for s, c in string_counts.items():
            if c <= 0:
                continue
            self._counts[s] = self._counts.get(s, 0) + int(c)
            self._consider_for_heap(s)

    def _cleanup_heap(self) -> None:
        '''
        Clean up outdated counts in heap and rebuild heap structure
        '''
        self._heap.clear()
        if self.m <= 0 or not self._in_heap_count:
            self._in_heap_count.clear()
            return
        # Rebuild heap from current in-heap mapping
        for s, c in self._in_heap_count.items():
            heapq.heappush(self._heap, (c, self._seq, s))
            self._seq += 1
        # If, for any reason, in-heap mapping exceeded m, trim it
        if len(self._in_heap_count) > self.m:
            # Evict smallest until size == m
            while len(self._in_heap_count) > self.m:
                self._evict_smallest_valid()

    def get_top_k(self, k: int) -> Set[str]:
        '''
        Return the set of top-k strings by occurrence count
        Args:
            k: Number of strings to return
        Returns:
            Set containing the top-k strings
        '''
        if k <= 0 or not self._in_heap_count:
            return set()
        # We only maintain top-m; return up to min(k, m) strings
        top_items = sorted(self._in_heap_count.items(),
                           key=lambda x: (-x[1], x[0]))
        return set(s for s, _ in top_items[:min(k, len(top_items))])

    def trim_to_m(self) -> None:
        '''
        Keep only the top-m strings by occurrence count, delete others
        '''
        if self.m <= 0:
            self._counts.clear()
            self._in_heap_count.clear()
            self._heap.clear()
            return

        # Ensure in-heap contains at most m entries
        if len(self._in_heap_count) > self.m:
            # Evict smallest until size == m
            # Sort ascending by count then by string for deterministic eviction
            items = sorted(self._in_heap_count.items(),
                           key=lambda x: (x[1], x[0]))
            to_remove = len(self._in_heap_count) - self.m
            for i in range(to_remove):
                s = items[i][0]
                if s in self._in_heap_count:
                    del self._in_heap_count[s]

        # Now filter counts to only those in in-heap
        keep = set(self._in_heap_count.keys())
        if keep:
            to_delete = [s for s in self._counts.keys() if s not in keep]
            for s in to_delete:
                del self._counts[s]
        else:
            # No items to keep
            self._counts.clear()

        # Rebuild heap to reflect the trimmed set
        self._cleanup_heap()

    def size(self) -> int:
        '''Return the number of strings currently stored'''
        return len(self._counts)

    def get_count(self, string: str) -> int:
        '''Get the occurrence count of a specific string'''
        return self._counts.get(string, 0)

    # Internal helpers

    def _consider_for_heap(self, s: str) -> None:
        if self.m <= 0:
            return
        c = self._counts[s]

        if s in self._in_heap_count:
            if c > self._in_heap_count[s]:
                # Update existing in-heap entry lazily by pushing a new tuple
                self._in_heap_count[s] = c
                heapq.heappush(self._heap, (c, self._seq, s))
                self._seq += 1
            return

        # Not currently in heap set
        if len(self._in_heap_count) < self.m:
            self._in_heap_count[s] = c
            heapq.heappush(self._heap, (c, self._seq, s))
            self._seq += 1
            return

        # Compare against smallest valid in-heap item
        root = self._peek_valid_root()
        if root is None:
            # Rebuilt inside _peek_valid_root, try again
            root = self._peek_valid_root()
        if root is None:
            # Heap is still empty (no in-heap items)
            self._in_heap_count[s] = c
            heapq.heappush(self._heap, (c, self._seq, s))
            self._seq += 1
            return

        min_count = root[0]
        if c > min_count:
            # Insert new and evict smallest valid
            self._in_heap_count[s] = c
            heapq.heappush(self._heap, (c, self._seq, s))
            self._seq += 1
            self._evict_smallest_valid()

    def _peek_valid_root(self) -> Optional[Tuple[int, int, str]]:
        # Remove stale roots
        while self._heap and self._in_heap_count.get(self._heap[0][2]) != self._heap[0][0]:
            heapq.heappop(self._heap)
        if not self._heap and self._in_heap_count:
            # Rebuild if heap exhausted but we still track in-heap items
            self._cleanup_heap()
        if not self._heap:
            return None
        return self._heap[0]

    def _evict_smallest_valid(self) -> Optional[Tuple[int, str]]:
        root = self._peek_valid_root()
        if root is None:
            return None
        count, _, s = heapq.heappop(self._heap)
        # Root must be valid at this point
        self._in_heap_count.pop(s, None)
        return (count, s)
