
from pathlib import Path
from typing import Any, Optional, Tuple
from functools import total_ordering
import psutil
import weakref
import sys
from collections import OrderedDict

# Define a Node class for the sake of completeness, assuming it's not provided


class Node:
    pass


@total_ordering
class CacheEntry:
    def __init__(self, key: Path, value: Tuple[Node, str], size: int):
        self.key = key
        self.value = value
        self.size = size
        self.access_time = 0

    def __lt__(self, other: 'CacheEntry') -> bool:
        return self.access_time < other.access_time

    def __eq__(self, other: 'CacheEntry') -> bool:
        return self.access_time == other.access_time


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
        self.cache: OrderedDict[Path, CacheEntry] = OrderedDict()
        self.current_memory_mb = 0
        self.entry_count = 0

    def __setitem__(self, key: Path, value: Tuple[Node, str]) -> None:
        '''Add or update an AST cache entry with automatic cleanup.'''
        # Estimate the size of the new entry
        size = sys.getsizeof(value)

        # Remove existing entry if it exists
        if key in self.cache:
            self._remove_entry(key)

        # Create a new entry
        entry = CacheEntry(key, value, size)
        self.cache[key] = entry
        self.current_memory_mb += size / (1024 * 1024)
        self.entry_count += 1

        # Mark as recently used
        self._mark_recently_used(key)

        # Enforce limits
        self._enforce_limits()

    def __getitem__(self, key: Path) -> Tuple[Node, str]:
        '''Get AST cache entry and mark as recently used.'''
        if key in self.cache:
            entry = self.cache[key]
            self._mark_recently_used(key)
            return entry.value
        else:
            raise KeyError(key)

    def __delitem__(self, key: Path) -> None:
        '''Remove entry from cache.'''
        self._remove_entry(key)

    def __contains__(self, key: Path) -> bool:
        '''Check if key exists in cache.'''
        return key in self.cache

    def items(self) -> Any:
        '''Return all cache items.'''
        return ((key, entry.value) for key, entry in self.cache.items())

    def _enforce_limits(self) -> None:
        '''Enforce cache size and memory limits by evicting old entries.'''
        while self.entry_count > self.max_entries or self._should_evict_for_memory():
            self._evict_oldest()

    def _should_evict_for_memory(self) -> bool:
        '''Check if we should evict entries due to memory pressure.'''
        return self.current_memory_mb > self.max_memory_mb

    def _mark_recently_used(self, key: Path) -> None:
        '''Mark an entry as recently used by moving it to the end of the ordered dict.'''
        entry = self.cache.pop(key)
        entry.access_time = len(self.cache)
        self.cache[key] = entry

    def _remove_entry(self, key: Path) -> None:
        '''Remove an entry from the cache and update memory usage.'''
        if key in self.cache:
            entry = self.cache.pop(key)
            self.current_memory_mb -= entry.size / (1024 * 1024)
            self.entry_count -= 1

    def _evict_oldest(self) -> None:
        '''Evict the oldest entry from the cache.'''
        key, entry = self.cache.popitem(last=False)
        self.current_memory_mb -= entry.size / (1024 * 1024)
        self.entry_count -= 1
