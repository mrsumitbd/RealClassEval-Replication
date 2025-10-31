from collections import defaultdict
import heapq
from typing import List, Set

class TopKStringTracker:
    """
    Efficient Top-K string tracking data structure

    Core ideas:
    1. Use hash table to record string counts
    2. Use min-heap to maintain top-m strings (heap root is the m-th largest element)
    3. Lazy cleanup: avoid frequent heap operations
    """

    def __init__(self, m: int):
        """
        Initialize the data structure

        Args:
            m: Maximum number of strings to retain
        """
        self.m = m
        self.count = defaultdict(int)
        self.heap = []
        self.in_heap = set()

    def add_strings(self, strings: List[str]) -> None:
        """
        Add k strings to the data structure

        Args:
            strings: List of strings to add
        """
        string_counts = defaultdict(int)
        for s in strings:
            string_counts[s] += 1
        self.add_string_dict(dict(string_counts))

    def add_string_dict(self, string_counts: dict) -> None:
        """
        Add strings with their counts from a dictionary

        Args:
            string_counts: Dictionary mapping strings to their occurrence counts
        """
        for string, count in string_counts.items():
            if count <= 0:
                continue
            self.count[string] += count
            if string in self.in_heap:
                continue
            if len(self.heap) < self.m:
                heapq.heappush(self.heap, (self.count[string], string))
                self.in_heap.add(string)
            else:
                min_count, min_string = self.heap[0]
                if self.count[string] > min_count:
                    heapq.heappop(self.heap)
                    self.in_heap.remove(min_string)
                    heapq.heappush(self.heap, (self.count[string], string))
                    self.in_heap.add(string)
        self._cleanup_heap()

    def _cleanup_heap(self) -> None:
        """
        Clean up outdated counts in heap and rebuild heap structure
        """
        current_items = []
        for count, string in self.heap:
            if string in self.count:
                current_items.append((self.count[string], string))
        self.heap = []
        self.in_heap = set()
        current_items.sort(reverse=True)
        for count, string in current_items[:self.m]:
            heapq.heappush(self.heap, (count, string))
            self.in_heap.add(string)

    def get_top_k(self, k: int) -> Set[str]:
        """
        Return the set of top-k strings by occurrence count

        Args:
            k: Number of strings to return

        Returns:
            Set containing the top-k strings
        """
        all_items = [(count, string) for string, count in self.count.items()]
        all_items.sort(reverse=True, key=lambda x: x[0])
        return {string for _, string in all_items[:k]}

    def trim_to_m(self) -> None:
        """
        Keep only the top-m strings by occurrence count, delete others
        """
        if len(self.count) <= self.m:
            return
        all_items = [(count, string) for string, count in self.count.items()]
        all_items.sort(reverse=True, key=lambda x: x[0])
        top_m_strings = {string for _, string in all_items[:self.m]}
        new_count = defaultdict(int)
        for s in top_m_strings:
            new_count[s] = self.count[s]
        self.count = new_count
        self.heap = [(self.count[s], s) for s in top_m_strings]
        heapq.heapify(self.heap)
        self.in_heap = set(top_m_strings)

    def size(self) -> int:
        """Return the number of strings currently stored"""
        return len(self.count)

    def get_count(self, string: str) -> int:
        """Get the occurrence count of a specific string"""
        return self.count.get(string, 0)