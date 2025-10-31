
from pathlib import Path
from typing import Any
from collections import OrderedDict
import sys


class Node:  # Assuming Node is a class, if not replace with actual type
    pass


class BoundedASTCache:

    def __init__(self, max_entries: int = 1000, max_memory_mb: int = 500):
        self.max_entries = max_entries
        self.max_memory_mb = max_memory_mb
        self.cache = OrderedDict()
        self.current_memory = 0

    def __setitem__(self, key: Path, value: tuple[Node, str]) -> None:
        node, _ = value
        size = sys.getsizeof(node)
        if key in self.cache:
            self.current_memory -= sys.getsizeof(self.cache[key][0])
        self.cache[key] = value
        self.current_memory += size
        self._enforce_limits()

    def __getitem__(self, key: Path) -> tuple[Node, str]:
        value = self.cache.pop(key)
        self.cache[key] = value  # Move to end to mark as recently used
        return value

    def __delitem__(self, key: Path) -> None:
        if key in self.cache:
            self.current_memory -= sys.getsizeof(self.cache[key][0])
            del self.cache[key]

    def __contains__(self, key: Path) -> bool:
        return key in self.cache

    def items(self) -> Any:
        return self.cache.items()

    def _enforce_limits(self) -> None:
        while len(self.cache) > self.max_entries or self._should_evict_for_memory():
            key, value = self.cache.popitem(last=False)  # Remove oldest item
            self.current_memory -= sys.getsizeof(value[0])

    def _should_evict_for_memory(self) -> bool:
        return self.current_memory > self.max_memory_mb * 1024 * 1024
