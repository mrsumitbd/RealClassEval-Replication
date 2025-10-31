
from pathlib import Path
from typing import Any, Dict, Tuple, Optional
import os
import sys


class BoundedASTCache:

    def __init__(self, max_entries: int = 1000, max_memory_mb: int = 500):
        self.max_entries = max_entries
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.cache: Dict[Path, Tuple[Node, str]] = {}
        self.current_memory_usage = 0

    def __setitem__(self, key: Path, value: Tuple[Node, str]) -> None:
        if key in self.cache:
            self.current_memory_usage -= sys.getsizeof(self.cache[key])
        self.cache[key] = value
        self.current_memory_usage += sys.getsizeof(value)
        self._enforce_limits()

    def __getitem__(self, key: Path) -> Tuple[Node, str]:
        return self.cache[key]

    def __delitem__(self, key: Path) -> None:
        if key in self.cache:
            self.current_memory_usage -= sys.getsizeof(self.cache[key])
            del self.cache[key]

    def __contains__(self, key: Path) -> bool:
        return key in self.cache

    def items(self) -> Any:
        return self.cache.items()

    def _enforce_limits(self) -> None:
        while len(self.cache) > self.max_entries or self._should_evict_for_memory():
            self._evict_least_recently_used()

    def _should_evict_for_memory(self) -> bool:
        return self.current_memory_usage > self.max_memory_bytes

    def _evict_least_recently_used(self) -> None:
        if self.cache:
            lru_key = min(self.cache, key=self.cache.get)
            self.__delitem__(lru_key)
