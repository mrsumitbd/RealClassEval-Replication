
import os
from pathlib import Path
from typing import Any, Optional, Tuple, Dict
import sys
from collections import OrderedDict

Node = Any  # Placeholder for AST node type


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
        self._cache: Dict[Path, Tuple[Node, str]] = OrderedDict()

    def __setitem__(self, key: Path, value: Tuple[Node, str]) -> None:
        '''Add or update an AST cache entry with automatic cleanup.'''
        if key in self._cache:
            del self._cache[key]
        self._cache[key] = value
        self._enforce_limits()

    def __getitem__(self, key: Path) -> Tuple[Node, str]:
        '''Get AST cache entry and mark as recently used.'''
        value = self._cache.pop(key)
        self._cache[key] = value
        return value

    def __delitem__(self, key: Path) -> None:
        '''Remove entry from cache.'''
        del self._cache[key]

    def __contains__(self, key: Path) -> bool:
        '''Check if key exists in cache.'''
        return key in self._cache

    def items(self) -> Any:
        '''Return all cache items.'''
        return self._cache.items()

    def _enforce_limits(self) -> None:
        '''Enforce cache size and memory limits by evicting old entries.'''
        while len(self._cache) > self.max_entries or self._should_evict_for_memory():
            if not self._cache:
                break
            self._cache.popitem(last=False)

    def _should_evict_for_memory(self) -> bool:
        '''Check if we should evict entries due to memory pressure.'''
        if sys.platform == 'linux' or sys.platform == 'linux2':
            import resource
            usage = resource.getrusage(
                resource.RUSAGE_SELF).ru_maxrss * 1024  # KB to bytes
        elif sys.platform == 'darwin':
            import resource
            usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss  # bytes
        elif sys.platform == 'win32':
            import psutil
            usage = psutil.Process().memory_info().rss
        else:
            # Fallback for other platforms
            return False

        return usage > self.max_memory_bytes
