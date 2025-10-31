
import sys
import psutil
from pathlib import Path
from collections import OrderedDict
from typing import Any, Tuple
from ast import AST as Node


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
        self.max_entries = max_entries
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self._cache: OrderedDict[Path, Tuple[Node, str]] = OrderedDict()

    def __setitem__(self, key: Path, value: Tuple[Node, str]) -> None:
        '''Add or update an AST cache entry with automatic cleanup.'''
        if key in self._cache:
            # Update existing entry and move to end
            self._cache.pop(key)
        self._cache[key] = value
        self._cache.move_to_end(key)
        self._enforce_limits()

    def __getitem__(self, key: Path) -> Tuple[Node, str]:
        '''Get AST cache entry and mark as recently used.'''
        if key not in self._cache:
            raise KeyError(key)
        value = self._cache.pop(key)
        self._cache[key] = value
        self._cache.move_to_end(key)
        return value

    def __delitem__(self, key: Path) -> None:
        '''Remove entry from cache.'''
        self._cache.pop(key, None)

    def __contains__(self, key: Path) -> bool:
        '''Check if key exists in cache.'''
        return key in self._cache

    def items(self) -> Any:
        '''Return all cache items.'''
        return self._cache.items()

    def _enforce_limits(self) -> None:
        '''Enforce cache size and memory limits by evicting old entries.'''
        # Evict based on entry count
        while len(self._cache) > self.max_entries:
            self._cache.popitem(last=False)

        # Evict based on memory pressure
        while self._should_evict_for_memory() and self._cache:
            self._cache.popitem(last=False)

    def _should_evict_for_memory(self) -> bool:
        '''Check if we should evict entries due to memory pressure.'''
        # Use system memory usage as a proxy for overall pressure
        mem = psutil.virtual_memory()
        return mem.used > self.max_memory_bytes
