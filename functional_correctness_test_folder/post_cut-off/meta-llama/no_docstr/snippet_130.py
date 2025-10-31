
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
        self.current_memory_mb = 0

    def __setitem__(self, key: Path, value: tuple[Node, str]) -> None:
        if key in self.cache:
            self._remove_from_memory(key)
        self.cache[key] = value
        self._add_to_memory(key, value)
        self._enforce_limits()

    def __getitem__(self, key: Path) -> tuple[Node, str]:
        if key in self.cache:
            value = self.cache.pop(key)
            self.cache[key] = value  # Move to end to mark as recently used
            return value
        else:
            raise KeyError(key)

    def __delitem__(self, key: Path) -> None:
        if key in self.cache:
            self._remove_from_memory(key)
            del self.cache[key]

    def __contains__(self, key: Path) -> bool:
        return key in self.cache

    def items(self) -> Any:
        return self.cache.items()

    def _enforce_limits(self) -> None:
        while len(self.cache) > self.max_entries or self._should_evict_for_memory():
            key, value = self.cache.popitem(last=False)  # Remove oldest item
            self._remove_from_memory(key, value)

    def _should_evict_for_memory(self) -> bool:
        return self.current_memory_mb > self.max_memory_mb

    def _add_to_memory(self, key: Path, value: tuple[Node, str]) -> None:
        self.current_memory_mb += sys.getsizeof(key) + sys.getsizeof(value)

    def _remove_from_memory(self, key: Path, value: tuple[Node, str] = None) -> None:
        if value is None:
            value = self.cache[key]
        self.current_memory_mb -= sys.getsizeof(key) + sys.getsizeof(value)
