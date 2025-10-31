
import sys
from pathlib import Path
from typing import Any, Dict, Tuple
from collections import OrderedDict


class BoundedASTCache:
    def __init__(self, max_entries: int = 1000, max_memory_mb: int = 500):
        self.max_entries = max_entries
        self.max_memory_mb = max_memory_mb
        self.cache: OrderedDict[Path, Tuple[Node, str]] = OrderedDict()
        self.current_memory_mb = 0

    def __setitem__(self, key: Path, value: Tuple[Node, str]) -> None:
        if key in self.cache:
            del self.cache[key]
        self.cache[key] = value
        self.current_memory_mb += sys.getsizeof(value) / (1024 * 1024)
        self._enforce_limits()

    def __getitem__(self, key: Path) -> Tuple[Node, str]:
        value = self.cache.pop(key)
        self.cache[key] = value
        return value

    def __delitem__(self, key: Path) -> None:
        value = self.cache.pop(key)
        self.current_memory_mb -= sys.getsizeof(value) / (1024 * 1024)

    def __contains__(self, key: Path) -> bool:
        return key in self.cache

    def items(self) -> Any:
        return self.cache.items()

    def _enforce_limits(self) -> None:
        while len(self.cache) > self.max_entries or self._should_evict_for_memory():
            key, value = self.cache.popitem(last=False)
            self.current_memory_mb -= sys.getsizeof(value) / (1024 * 1024)

    def _should_evict_for_memory(self) -> bool:
        return self.current_memory_mb > self.max_memory_mb
