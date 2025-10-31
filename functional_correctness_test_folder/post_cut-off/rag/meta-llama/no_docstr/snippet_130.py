
from pathlib import Path
from typing import Any, Optional, Tuple
from collections import OrderedDict
import psutil
import logging

Node = Any  # Assuming Node is defined elsewhere


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
        self.max_memory_mb = max_memory_mb
        self.cache: OrderedDict[Path, Tuple[Node, str]] = OrderedDict()
        self.current_memory_mb = 0

    def __setitem__(self, key: Path, value: Tuple[Node, str]) -> None:
        '''Add or update an AST cache entry with automatic cleanup.'''
        if key in self.cache:
            self._remove_from_memory(key)
        self.cache[key] = value
        self._add_to_memory(key)
        self._enforce_limits()

    def __getitem__(self, key: Path) -> Tuple[Node, str]:
        '''Get AST cache entry and mark as recently used.'''
        value = self.cache.pop(key)
        self.cache[key] = value  # Move to end to mark as recently used
        return value

    def __delitem__(self, key: Path) -> None:
        '''Remove entry from cache.'''
        if key in self.cache:
            self._remove_from_memory(key)
            del self.cache[key]

    def __contains__(self, key: Path) -> bool:
        '''Check if key exists in cache.'''
        return key in self.cache

    def items(self) -> Any:
        '''Return all cache items.'''
        return self.cache.items()

    def _enforce_limits(self) -> None:
        '''Enforce cache size and memory limits by evicting old entries.'''
        while len(self.cache) > self.max_entries:
            self._evict_oldest()
        while self._should_evict_for_memory():
            self._evict_oldest()

    def _should_evict_for_memory(self) -> bool:
        '''Check if we should evict entries due to memory pressure.'''
        process = psutil.Process()
        self.current_memory_mb = process.memory_info().rss / (1024 * 1024)
        return self.current_memory_mb > self.max_memory_mb

    def _evict_oldest(self) -> None:
        '''Evict the oldest entry from the cache.'''
        key, value = self.cache.popitem(last=False)
        self._remove_from_memory(key)

    def _add_to_memory(self, key: Path) -> None:
        '''Estimate and add the memory usage of the given key-value pair.'''
        # For simplicity, assume the memory usage is the size of the value
        # In a real implementation, you might need a more sophisticated way to estimate memory usage
        value = self.cache[key]
        # Assuming value is a tuple of (Node, str)
        self.current_memory_mb += (sys.getsizeof(
            value[0]) + sys.getsizeof(value[1])) / (1024 * 1024)

    def _remove_from_memory(self, key: Path) -> None:
        '''Estimate and subtract the memory usage of the given key-value pair.'''
        # For simplicity, assume the memory usage is the size of the value
        # In a real implementation, you might need a more sophisticated way to estimate memory usage
        if key in self.cache:
            value = self.cache[key]
            # Assuming value is a tuple of (Node, str)
            self.current_memory_mb -= (sys.getsizeof(
                value[0]) + sys.getsizeof(value[1])) / (1024 * 1024)
            if self.current_memory_mb < 0:
                self.current_memory_mb = 0
                logging.warning(
                    "Memory usage went below 0, this should not happen.")
