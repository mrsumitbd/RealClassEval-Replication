
from __future__ import annotations

import sys
from collections import OrderedDict
from pathlib import Path
from typing import Any, Tuple

import ast

# Type alias for clarity
ASTEntry = Tuple[ast.AST, str]


class BoundedASTCache:
    """Memory‑aware AST cache with automatic cleanup to prevent memory leaks.
    Uses LRU eviction strategy and monitors memory usage to maintain
    reasonable memory consumption during long‑running analysis sessions.
    """

    def __init__(self, max_entries: int = 1000, max_memory_mb: int = 500):
        """Initialize the bounded AST cache.

        Args:
            max_entries: Maximum number of AST entries to cache
            max_memory_mb: Soft memory limit in MB for cache eviction
        """
        self.max_entries = max_entries
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self._cache: OrderedDict[Path, ASTEntry] = OrderedDict()
        self._entry_sizes: dict[Path, int] = {}
        self._total_size: int = 0

    def __setitem__(self, key: Path, value: ASTEntry) -> None:
        """Add or update an AST cache entry with automatic cleanup."""
        # If key already exists, remove old size
        if key in self._cache:
            self._total_size -= self._entry_sizes[key]
        # Store entry
        self._cache[key] = value
        # Move to end to mark as most recently used
        self._cache.move_to_end(key)
        # Estimate size
        size = (
            sys.getsizeof(value[0])  # AST node
            + sys.getsizeof(value[1])  # source string
            + sys.getsizeof(value)  # tuple overhead
        )
        self._entry_sizes[key] = size
        self._total_size += size
        # Enforce limits
        self._enforce_limits()

    def __getitem__(self, key: Path) -> ASTEntry:
        """Get AST cache entry and mark as recently used."""
        if key not in self._cache:
            raise KeyError(key)
        # Move to end to mark as recently used
        self._cache.move_to_end(key)
        return self._cache[key]

    def __delitem__(self, key: Path) -> None:
        """Remove entry from cache."""
        if key in self._cache:
            self._total_size -= self._entry_sizes.pop(key)
            del self._cache[key]

    def __contains__(self, key: Path) -> bool:
        """Check if key exists in cache."""
        return key in self._cache

    def items(self) -> Any:
        """Return all cache items."""
        return self._cache.items()

    def _enforce_limits(self) -> None:
        """Enforce cache size and memory limits by evicting old entries."""
        # Evict based on entry count
        while len(self._cache) > self.max_entries:
            self._evict_oldest()
        # Evict based on memory usage
        while self._should_evict_for_memory():
            self._evict_oldest()

    def _should_evict_for_memory(self) -> bool:
        """Check if we should evict entries due to memory pressure."""
        return self._total_size > self.max_memory_bytes

    def _evict_oldest(self) -> None:
        """Evict the least recently used entry."""
        key, _ = self._cache.popitem(last=False)
        self._total_size -= self._entry_sizes.pop(key, 0)
