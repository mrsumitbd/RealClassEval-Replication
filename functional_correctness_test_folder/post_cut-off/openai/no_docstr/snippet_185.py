
from typing import List, Set, Dict
import heapq


class TopKStringTracker:
    def __init__(self, m: int):
        """
        Initialize the tracker with a maximum capacity `m`.
        """
        self._max_size = m
        self._counts: Dict[str, int] = {}

    def add_strings(self, strings: List[str]) -> None:
        """
        Increment the count for each string in the provided list.
        """
        for s in strings:
            self._counts[s] = self._counts.get(s, 0) + 1

    def add_string_dict(self, string_counts: dict) -> None:
        """
        Increment counts based on a dictionary of string -> count.
        """
        for s, c in string_counts.items():
            self._counts[s] = self._counts.get(s, 0) + c

    def _cleanup_heap(self) -> None:
        """
        No-op for this implementation. Included for API compatibility.
        """
        pass

    def get_top_k(self, k: int) -> Set[str]:
        """
        Return a set of the top `k` strings by count.
        """
        if k <= 0:
            return set()
        # Use nlargest to get the k highest counts
        top_k = heapq.nlargest(k, self._counts.items(),
                               key=lambda item: item[1])
        return {s for s, _ in top_k}

    def trim_to_m(self) -> None:
        """
        Trim the internal dictionary to keep only the top `m` strings.
        """
        if self._max_size <= 0:
            self._counts.clear()
            return
        # Get the top m items
        top_m = heapq.nlargest(
            self._max_size, self._counts.items(), key=lambda item: item[1])
        # Rebuild the dictionary with only those items
        self._counts = {s: c for s, c in top_m}

    def size(self) -> int:
        """
        Return the number of distinct strings currently tracked.
        """
        return len(self._counts)

    def get_count(self, string: str) -> int:
        """
        Return the count for a specific string, or 0 if not present.
        """
        return self._counts.get(string, 0)
