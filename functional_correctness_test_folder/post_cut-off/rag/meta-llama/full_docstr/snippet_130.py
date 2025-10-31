
from pathlib import Path
from typing import Any, Optional, Tuple
from collections import OrderedDict
import psutil
import os
from .ast_nodes import Node


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
            self._remove_from_memory_count(self.cache[key])
        self.cache[key] = value
        self._add_to_memory_count(value)
        self._enforce_limits()

    def __getitem__(self, key: Path) -> Tuple[Node, str]:
        '''Get AST cache entry and mark as recently used.'''
        value = self.cache.pop(key)
        self.cache[key] = value  # Move to end to mark as recently used
        return value

    def __delitem__(self, key: Path) -> None:
        '''Remove entry from cache.'''
        if key in self.cache:
            self._remove_from_memory_count(self.cache[key])
            del self.cache[key]

    def __contains__(self, key: Path) -> bool:
        '''Check if key exists in cache.'''
        return key in self.cache

    def items(self) -> Any:
        '''Return all cache items.'''
        return self.cache.items()

    def _enforce_limits(self) -> None:
        '''Enforce cache size and memory limits by evicting old entries.'''
        while len(self.cache) > self.max_entries or self._should_evict_for_memory():
            key, value = self.cache.popitem(last=False)  # Remove oldest item
            self._remove_from_memory_count(value)

    def _should_evict_for_memory(self) -> bool:
        '''Check if we should evict entries due to memory pressure.'''
        process = psutil.Process(os.getpid())
        self.current_memory_mb = process.memory_info().rss / (1024 * 1024)
        return self.current_memory_mb > self.max_memory_mb

    def _add_to_memory_count(self, value: Tuple[Node, str]) -> None:
        '''Approximately count the memory usage of the given value.'''
        # For simplicity, we just count the size of the string representation
        # In a real implementation, you might want to use a more accurate method
        self.current_memory_mb += len(str(value)) / (1024 * 1024)

    def _remove_from_memory_count(self, value: Tuple[Node, str]) -> None:
        '''Approximately subtract the memory usage of the given value from the count.'''
        # For simplicity, we just count the size of the string representation
        # In a real implementation, you might want to use a more accurate method
        self.current_memory_mb -= len(str(value)) / (1024 * 1024)
        self.current_memory_mb = max(
            0, self.current_memory_mb)  # Ensure non-negative
