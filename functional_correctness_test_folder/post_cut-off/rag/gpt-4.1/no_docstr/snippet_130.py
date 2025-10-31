import sys
import threading
from collections import OrderedDict
from pathlib import Path
from typing import Any, Tuple

try:
    import psutil
except ImportError:
    psutil = None

# Assume Node is a type representing an AST node
try:
    from ast import AST as Node
except ImportError:
    Node = object  # fallback


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
        self._cache: OrderedDict[Path, Tuple[Node, str]] = OrderedDict()
        self._max_entries = max_entries
        self._max_memory_mb = max_memory_mb
        self._lock = threading.RLock()

    def __setitem__(self, key: Path, value: tuple[Node, str]) -> None:
        '''Add or update an AST cache entry with automatic cleanup.'''
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            self._cache[key] = value
            self._enforce_limits()

    def __getitem__(self, key: Path) -> tuple[Node, str]:
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
        # Evict by LRU if over max_entries
        with self._lock:
            while len(self._cache) > self._max_entries:
                self._cache.popitem(last=False)
            # Evict for memory pressure
            while self._should_evict_for_memory() and self._cache:
                self._cache.popitem(last=False)

    def _should_evict_for_memory(self) -> bool:
        '''Check if we should evict entries due to memory pressure.'''
        if psutil is not None:
            process = psutil.Process()
            mem_bytes = process.memory_info().rss
            mem_mb = mem_bytes / (1024 * 1024)
            return mem_mb > self._max_memory_mb
        else:
            # Fallback: use sys.getsizeof for the cache (not accurate for ASTs)
            size = sys.getsizeof(self._cache)
            for k, v in self._cache.items():
                size += sys.getsizeof(k)
                size += sys.getsizeof(v)
            mem_mb = size / (1024 * 1024)
            return mem_mb > self._max_memory_mb
