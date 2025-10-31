from collections import OrderedDict, defaultdict
from tree_sitter import Node, Parser
from pathlib import Path
import sys
from typing import Any

class BoundedASTCache:
    """Memory-aware AST cache with automatic cleanup to prevent memory leaks.

    Uses LRU eviction strategy and monitors memory usage to maintain
    reasonable memory consumption during long-running analysis sessions.
    """

    def __init__(self, max_entries: int=1000, max_memory_mb: int=500):
        """Initialize the bounded AST cache.

        Args:
            max_entries: Maximum number of AST entries to cache
            max_memory_mb: Soft memory limit in MB for cache eviction
        """
        self.cache: OrderedDict[Path, tuple[Node, str]] = OrderedDict()
        self.max_entries = max_entries
        self.max_memory_bytes = max_memory_mb * 1024 * 1024

    def __setitem__(self, key: Path, value: tuple[Node, str]) -> None:
        """Add or update an AST cache entry with automatic cleanup."""
        if key in self.cache:
            del self.cache[key]
        self.cache[key] = value
        self._enforce_limits()

    def __getitem__(self, key: Path) -> tuple[Node, str]:
        """Get AST cache entry and mark as recently used."""
        value = self.cache[key]
        self.cache.move_to_end(key)
        return value

    def __delitem__(self, key: Path) -> None:
        """Remove entry from cache."""
        if key in self.cache:
            del self.cache[key]

    def __contains__(self, key: Path) -> bool:
        """Check if key exists in cache."""
        return key in self.cache

    def items(self) -> Any:
        """Return all cache items."""
        return self.cache.items()

    def _enforce_limits(self) -> None:
        """Enforce cache size and memory limits by evicting old entries."""
        while len(self.cache) > self.max_entries:
            self.cache.popitem(last=False)
        if self._should_evict_for_memory():
            entries_to_remove = max(1, len(self.cache) // 10)
            for _ in range(entries_to_remove):
                if self.cache:
                    self.cache.popitem(last=False)

    def _should_evict_for_memory(self) -> bool:
        """Check if we should evict entries due to memory pressure."""
        try:
            cache_size = sum((sys.getsizeof(v) for v in self.cache.values()))
            return cache_size > self.max_memory_bytes
        except Exception:
            return len(self.cache) > self.max_entries * 0.8