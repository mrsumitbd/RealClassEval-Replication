
from collections import OrderedDict
from pathlib import Path
from typing import Any, Tuple
import psutil
import sys

Node = Any  # Assuming Node is a type, replace with actual type if available


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
        self.cache = OrderedDict()

    def __setitem__(self, key: Path, value: Tuple[Node, str]) -> None:
        '''Add or update an AST cache entry with automatic cleanup.'''
        if key in self.cache:
            del self.cache[key]
        self.cache[key] = value
        self._enforce_limits()

    def __getitem__(self, key: Path) -> Tuple[Node, str]:
        '''Get AST cache entry and mark as recently used.'''
        value = self.cache.pop(key)
        self.cache[key] = value  # Set key as most recently used
        return value

    def __delitem__(self, key: Path) -> None:
        '''Remove entry from cache.'''
        if key in self.cache:
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
            self.cache.popitem(last=False)  # Remove oldest item

    def _should_evict_for_memory(self) -> bool:
        '''Check if we should evict entries due to memory pressure.'''
        process = psutil.Process()
        mem_usage_mb = process.memory_info().rss / (1024 * 1024)
        return mem_usage_mb > self.max_memory_mb


# Example usage:
if __name__ == "__main__":
    cache = BoundedASTCache(max_entries=100, max_memory_mb=200)
    key = Path("example.py")
    # Replace with actual Node and source code
    value = (None, "example_source_code")
    cache[key] = value
    print(key in cache)
    print(cache[key])
    del cache[key]
    print(key in cache)
    for k, v in cache.items():
        print(k, v)
