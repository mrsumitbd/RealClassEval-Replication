
from pathlib import Path
from typing import Any, Tuple, Dict, Iterator
from collections import OrderedDict
import sys

# Dummy Node class for type hinting; replace with actual Node if available


class Node:
    pass


class BoundedASTCache:
    def __init__(self, max_entries: int = 1000, max_memory_mb: int = 500):
        self.max_entries = max_entries
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self._cache: "OrderedDict[Path, Tuple[Node, str]]" = OrderedDict()
        self._memory_usage = 0
        self._memory_sizes: Dict[Path, int] = {}

    def __setitem__(self, key: Path, value: tuple[Node, str]) -> None:
        if key in self._cache:
            self.__delitem__(key)
        self._cache[key] = value
        size = self._estimate_size(key, value)
        self._memory_sizes[key] = size
        self._memory_usage += size
        self._cache.move_to_end(key)
        self._enforce_limits()

    def __getitem__(self, key: Path) -> tuple[Node, str]:
        value = self._cache[key]
        self._cache.move_to_end(key)
        return value

    def __delitem__(self, key: Path) -> None:
        if key in self._cache:
            size = self._memory_sizes.pop(key, 0)
            self._memory_usage -= size
            del self._cache[key]

    def __contains__(self, key: Path) -> bool:
        '''Check if key exists in cache.'''
        return key in self._cache

    def items(self) -> Iterator[Tuple[Path, tuple[Node, str]]]:
        return self._cache.items()

    def _enforce_limits(self) -> None:
        '''Enforce cache size and memory limits by evicting old entries.'''
        while (len(self._cache) > self.max_entries) or self._should_evict_for_memory():
            old_key, _ = self._cache.popitem(last=False)
            size = self._memory_sizes.pop(old_key, 0)
            self._memory_usage -= size

    def _should_evict_for_memory(self) -> bool:
        return self._memory_usage > self.max_memory_bytes

    def _estimate_size(self, key: Path, value: tuple[Node, str]) -> int:
        # Estimate memory usage of the cache entry
        node, code = value
        size = sys.getsizeof(key)
        size += sys.getsizeof(code)
        size += sys.getsizeof(node)
        # Optionally, add more detailed estimation for node and code
        return size
