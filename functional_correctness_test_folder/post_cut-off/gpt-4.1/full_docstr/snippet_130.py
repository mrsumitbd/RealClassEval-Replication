
from collections import OrderedDict
from pathlib import Path
from typing import Any, Tuple
import sys
import threading

# Dummy Node type for type hinting; replace with actual AST Node if needed


class Node:
    pass


class BoundedASTCache:
    '''Memory-aware AST cache with automatic cleanup to prevent memory leaks.
    Uses LRU eviction strategy and monitors memory usage to maintain
    reasonable memory consumption during long-running analysis sessions.
    '''

    def __init__(self, max_entries: int = 1000, max_memory_mb: int = 500):
        '''Initialize the bounded AST cache.
        Args:
            max_entries: Maximum number of AST entries to cache
            max_memory_mb: Soft memory limit in MB for cache eviction
        '''
        self._cache = OrderedDict(
        )  # type: OrderedDict[Path, tuple[Node, str]]
        self._max_entries = max_entries
        self._max_memory_bytes = max_memory_mb * 1024 * 1024
        self._lock = threading.RLock()
        self._total_size = 0
        self._sizes = {}  # type: dict[Path, int]

    def __setitem__(self, key: Path, value: Tuple[Node, str]) -> None:
        '''Add or update an AST cache entry with automatic cleanup.'''
        with self._lock:
            if key in self._cache:
                self._total_size -= self._sizes.get(key, 0)
                del self._cache[key]
                del self._sizes[key]
            self._cache[key] = value
            size = self._estimate_entry_size(key, value)
            self._sizes[key] = size
            self._total_size += size
            self._cache.move_to_end(key)
            self._enforce_limits()

    def __getitem__(self, key: Path) -> Tuple[Node, str]:
        '''Get AST cache entry and mark as recently used.'''
        with self._lock:
            value = self._cache[key]
            self._cache.move_to_end(key)
            return value

    def __delitem__(self, key: Path) -> None:
        '''Remove entry from cache.'''
        with self._lock:
            if key in self._cache:
                self._total_size -= self._sizes.get(key, 0)
                del self._cache[key]
                del self._sizes[key]

    def __contains__(self, key: Path) -> bool:
        '''Check if key exists in cache.'''
        with self._lock:
            return key in self._cache

    def items(self) -> Any:
        '''Return all cache items.'''
        with self._lock:
            return list(self._cache.items())

    def _enforce_limits(self) -> None:
        '''Enforce cache size and memory limits by evicting old entries.'''
        with self._lock:
            # Evict by entry count
            while len(self._cache) > self._max_entries:
                old_key, _ = self._cache.popitem(last=False)
                self._total_size -= self._sizes.get(old_key, 0)
                self._sizes.pop(old_key, None)
            # Evict by memory
            while self._should_evict_for_memory() and self._cache:
                old_key, _ = self._cache.popitem(last=False)
                self._total_size -= self._sizes.get(old_key, 0)
                self._sizes.pop(old_key, None)

    def _should_evict_for_memory(self) -> bool:
        '''Check if we should evict entries due to memory pressure.'''
        return self._total_size > self._max_memory_bytes

    def _estimate_entry_size(self, key: Path, value: Tuple[Node, str]) -> int:
        '''Estimate the memory size of a cache entry.'''
        node, code = value
        size = 0
        try:
            size += sys.getsizeof(key)
            size += sys.getsizeof(code)
            size += sys.getsizeof(node)
            # Optionally, try to estimate node size more deeply if needed
        except Exception:
            pass
        return size
