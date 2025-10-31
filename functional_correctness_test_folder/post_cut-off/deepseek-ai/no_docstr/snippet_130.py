
import os
from pathlib import Path
from typing import Any, Tuple, Dict, Optional
import sys
from collections import OrderedDict


class Node:
    pass  # Placeholder for the Node type


class BoundedASTCache:

    def __init__(self, max_entries: int = 1000, max_memory_mb: int = 500):
        self.max_entries = max_entries
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self._cache: OrderedDict[Path, Tuple[Node, str]] = OrderedDict()

    def __setitem__(self, key: Path, value: Tuple[Node, str]) -> None:
        if key in self._cache:
            del self._cache[key]
        self._cache[key] = value
        self._enforce_limits()

    def __getitem__(self, key: Path) -> Tuple[Node, str]:
        value = self._cache[key]
        self._cache.move_to_end(key)
        return value

    def __delitem__(self, key: Path) -> None:
        del self._cache[key]

    def __contains__(self, key: Path) -> bool:
        return key in self._cache

    def items(self) -> Any:
        return self._cache.items()

    def _enforce_limits(self) -> None:
        while len(self._cache) > self.max_entries or self._should_evict_for_memory():
            self._cache.popitem(last=False)

    def _should_evict_for_memory(self) -> bool:
        if self.max_memory_bytes <= 0:
            return False
        total_size = sum(sys.getsizeof(node) + sys.getsizeof(code)
                         for node, code in self._cache.values())
        return total_size > self.max_memory_bytes
