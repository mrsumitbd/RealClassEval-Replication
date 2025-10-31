
from pathlib import Path
from typing import Any, Dict, Tuple, Optional
import os
import heapq


class BoundedASTCache:

    def __init__(self, max_entries: int = 1000, max_memory_mb: int = 500):
        self.max_entries = max_entries
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.cache: Dict[Path, Tuple[Node, str, int]] = {}
        self.access_order: list = []
        self.current_memory_usage = 0

    def __setitem__(self, key: Path, value: Tuple[Node, str]) -> None:
        node, code = value
        memory_usage = self._get_memory_usage(node, code)
        if key in self.cache:
            self.current_memory_usage -= self.cache[key][2]
        self.cache[key] = (node, code, memory_usage)
        self.current_memory_usage += memory_usage
        self.access_order.append(key)
        self._enforce_limits()

    def __getitem__(self, key: Path) -> Tuple[Node, str]:
        if key not in self.cache:
            raise KeyError(f"Key {key} not found in cache.")
        self.access_order.remove(key)
        self.access_order.append(key)
        return self.cache[key][:2]

    def __delitem__(self, key: Path) -> None:
        if key in self.cache:
            self.current_memory_usage -= self.cache[key][2]
            del self.cache[key]
            self.access_order.remove(key)

    def __contains__(self, key: Path) -> bool:
        return key in self.cache

    def items(self) -> Any:
        return self.cache.items()

    def _enforce_limits(self) -> None:
        while len(self.cache) > self.max_entries or self._should_evict_for_memory():
            oldest_key = self.access_order.pop(0)
            del self.cache[oldest_key]
            self.current_memory_usage -= self.cache[oldest_key][2]

    def _should_evict_for_memory(self) -> bool:
        return self.current_memory_usage > self.max_memory_bytes

    def _get_memory_usage(self, node: Node, code: str) -> int:
        # Placeholder for actual memory usage calculation
        # This should be replaced with an actual implementation
        return os.sys.getsizeof(node) + os.sys.getsizeof(code)
