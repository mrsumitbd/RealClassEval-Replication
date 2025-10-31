
from pathlib import Path
from typing import Any, Tuple, Iterator
from collections import OrderedDict
import sys

# Dummy Node class for type hinting; replace with actual Node if available


class Node:
    pass


class BoundedASTCache:
    def __init__(self, max_entries: int = 1000, max_memory_mb: int = 500):
        self.max_entries = max_entries
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self._cache: OrderedDict[Path, Tuple[Node, str]] = OrderedDict()
        self._memory_usage = 0
        self._memory_sizes: dict[Path, int] = {}

    def __setitem__(self, key: Path, value: tuple[Node, str]) -> None:
        if key in self._cache:
            self._memory_usage -= self._memory_sizes[key]
            del self._cache[key]
            del self._memory_sizes[key]
        self._cache[key] = value
        mem_size = self._estimate_size(key, value)
        self._memory_sizes[key] = mem_size
        self._memory_usage += mem_size
        self._cache.move_to_end(key)
        self._enforce_limits()

    def __getitem__(self, key: Path) -> tuple[Node, str]:
        value = self._cache[key]
        self._cache.move_to_end(key)
        return value

    def __delitem__(self, key: Path) -> None:
        if key in self._cache:
            self._memory_usage -= self._memory_sizes[key]
            del self._cache[key]
            del self._memory_sizes[key]

    def __contains__(self, key: Path) -> bool:
        return key in self._cache

    def items(self) -> Iterator[tuple[Path, tuple[Node, str]]]:
        return self._cache.items()

    def _enforce_limits(self) -> None:
        # Evict by entry count
        while len(self._cache) > self.max_entries:
            old_key, _ = self._cache.popitem(last=False)
            self._memory_usage -= self._memory_sizes[old_key]
            del self._memory_sizes[old_key]
        # Evict by memory
        while self._should_evict_for_memory():
            old_key, _ = self._cache.popitem(last=False)
            self._memory_usage -= self._memory_sizes[old_key]
            del self._memory_sizes[old_key]

    def _should_evict_for_memory(self) -> bool:
        return self._memory_usage > self.max_memory_bytes

    def _estimate_size(self, key: Path, value: tuple[Node, str]) -> int:
        node, code = value
        size = sys.getsizeof(key)
        size += sys.getsizeof(code)
        size += sys.getsizeof(node)
        # Try to add more if node has __dict__ or __slots__
        if hasattr(node, '__dict__'):
            size += sys.getsizeof(node.__dict__)
        if hasattr(node, '__slots__'):
            for slot in node.__slots__:
                size += sys.getsizeof(getattr(node, slot, None))
        return size
