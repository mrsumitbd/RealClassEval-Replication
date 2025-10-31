
import sys
from pathlib import Path
from typing import Any, Dict, Tuple
from ast import Node


class BoundedASTCache:
    def __init__(self, max_entries: int = 1000, max_memory_mb: int = 500):
        self.max_entries = max_entries
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.cache: Dict[Path, Tuple[Node, str]] = {}
        self.access_order: Dict[Path, int] = {}
        self.access_counter = 0

    def __setitem__(self, key: Path, value: Tuple[Node, str]) -> None:
        if key in self.cache:
            del self.cache[key]
        self.cache[key] = value
        self.access_order[key] = self.access_counter
        self.access_counter += 1
        self._enforce_limits()

    def __getitem__(self, key: Path) -> Tuple[Node, str]:
        if key not in self.cache:
            raise KeyError(key)
        self.access_order[key] = self.access_counter
        self.access_counter += 1
        return self.cache[key]

    def __delitem__(self, key: Path) -> None:
        if key not in self.cache:
            raise KeyError(key)
        del self.cache[key]
        del self.access_order[key]

    def __contains__(self, key: Path) -> bool:
        return key in self.cache

    def items(self) -> Any:
        return self.cache.items()

    def _enforce_limits(self) -> None:
        while len(self.cache) > self.max_entries or self._should_evict_for_memory():
            least_recently_used_key = min(
                self.access_order, key=self.access_order.get)
            del self[least_recently_used_key]

    def _should_evict_for_memory(self) -> bool:
        current_memory = sum(sys.getsizeof(value)
                             for value in self.cache.values())
        return current_memory > self.max_memory_bytes
