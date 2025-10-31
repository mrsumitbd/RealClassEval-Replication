import threading
import sys
import collections
import psutil
from pathlib import Path
from typing import Any, Tuple

# Assume Node is defined elsewhere
# from some_ast_module import Node


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
        self._cache = collections.OrderedDict()  # type: ignore
        self._lock = threading.RLock()
        self._max_entries = max_entries
        self._max_memory_mb = max_memory_mb

    def __setitem__(self, key: Path, value: Tuple[Any, str]) -> None:
        '''Add or update an AST cache entry with automatic cleanup.'''
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            self._cache[key] = value
            self._enforce_limits()

    def __getitem__(self, key: Path) -> Tuple[Any, str]:
        '''Get AST cache entry and mark as recently used.'''
        with self._lock:
            value = self._cache[key]
            self._cache.move_to_end(key)
            return value

    def __delitem__(self, key: Path) -> None:
        '''Remove entry from cache.'''
        with self._lock:
            del self._cache[key]

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
            # Evict by LRU if too many entries
            while len(self._cache) > self._max_entries:
                self._cache.popitem(last=False)
            # Evict if memory usage is too high
            while self._should_evict_for_memory() and self._cache:
                self._cache.popitem(last=False)

    def _should_evict_for_memory(self) -> bool:
        '''Check if we should evict entries due to memory pressure.'''
        process = psutil.Process()
        mem_mb = process.memory_info().rss / (1024 * 1024)
        return mem_mb > self._max_memory_mb
