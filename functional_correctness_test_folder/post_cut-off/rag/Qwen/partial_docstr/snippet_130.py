
import os
from collections import OrderedDict
from pathlib import Path
from typing import Any, Tuple, Dict
import psutil


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
        self.cache: OrderedDict[Path, Tuple[Node, str]] = OrderedDict()
        self.max_entries = max_entries
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.current_memory_usage = 0

    def __setitem__(self, key: Path, value: Tuple[Node, str]) -> None:
        '''Add or update an AST cache entry with automatic cleanup.'''
        if key in self.cache:
            self.current_memory_usage -= self._get_item_size(self.cache[key])
        self.cache[key] = value
        self.current_memory_usage += self._get_item_size(value)
        self.cache.move_to_end(key)
        self._enforce_limits()

    def __getitem__(self, key: Path) -> Tuple[Node, str]:
        '''Get AST cache entry and mark as recently used.'''
        value = self.cache[key]
        self.cache.move_to_end(key)
        return value

    def __delitem__(self, key: Path) -> None:
        '''Remove entry from cache.'''
        value = self.cache.pop(key)
        self.current_memory_usage -= self._get_item_size(value)

    def __contains__(self, key: Path) -> bool:
        '''Check if key exists in cache.'''
        return key in self.cache

    def items(self) -> Any:
        '''Return all cache items.'''
        return self.cache.items()

    def _enforce_limits(self) -> None:
        '''Enforce cache size and memory limits by evicting old entries.'''
        while len(self.cache) > self.max_entries or self._should_evict_for_memory():
            key, value = self.cache.popitem(last=False)
            self.current_memory_usage -= self._get_item_size(value)

    def _should_evict_for_memory(self) -> bool:
        '''Check if we should evict entries due to memory pressure.'''
        return self.current_memory_usage > self.max_memory_bytes

    def _get_item_size(self, item: Tuple[Node, str]) -> int:
        '''Estimate the memory size of a cache item.'''
        node, string = item
        # Assuming Node has a __sizeof__ method or similar to estimate its size
        node_size = node.__sizeof__()
        string_size = len(string.encode('utf-8'))
        return node_size + string_size
