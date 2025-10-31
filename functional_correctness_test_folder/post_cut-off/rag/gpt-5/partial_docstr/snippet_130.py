from __future__ import annotations

from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, MutableMapping, Tuple, Optional, Iterable
import sys
import threading
import gc

try:
    import psutil  # type: ignore
except Exception:  # pragma: no cover
    psutil = None  # type: ignore


Node = Any


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
        self.max_entries = int(max_entries)
        self.max_memory_bytes = int(max_memory_mb) * 1024 * 1024

        self._cache: "OrderedDict[Path, tuple[Node, str]]" = OrderedDict()
        self._sizes: Dict[Path, int] = {}
        self._total_size: int = 0
        self._lock = threading.RLock()

    def __setitem__(self, key: Path, value: tuple[Node, str]) -> None:
        '''Add or update an AST cache entry with automatic cleanup.'''
        with self._lock:
            if key in self._cache:
                self._remove_no_lock(key)

            size = self._estimate_size(value)
            self._cache[key] = value
            self._cache.move_to_end(key, last=True)
            self._sizes[key] = size
            self._total_size += size

            self._enforce_limits()

    def __getitem__(self, key: Path) -> tuple[Node, str]:
        '''Get AST cache entry and mark as recently used.'''
        with self._lock:
            value = self._cache[key]
            self._cache.move_to_end(key, last=True)
            return value

    def __delitem__(self, key: Path) -> None:
        '''Remove entry from cache.'''
        with self._lock:
            self._remove_no_lock(key)

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
            # Evict based on entry count first
            while len(self._cache) > self.max_entries:
                self._evict_one_lru_no_lock()

            # Evict based on memory pressure
            while self._should_evict_for_memory() and self._cache:
                self._evict_one_lru_no_lock()

            # Encourage freeing memory promptly
            gc.collect()

    def _should_evict_for_memory(self) -> bool:
        '''Check if we should evict entries due to memory pressure.'''
        # Cache soft limit
        if self._total_size > self.max_memory_bytes:
            return True

        # Process-level soft limit (if psutil available)
        if psutil is not None:
            try:
                rss = psutil.Process().memory_info().rss
                if rss > self.max_memory_bytes:
                    return True
            except Exception:
                # If psutil check fails, fall back to cache-only check
                pass

        return False

    def _evict_one_lru_no_lock(self) -> None:
        # Pop least-recently-used item (left side)
        key, _ = self._cache.popitem(last=False)
        size = self._sizes.pop(key, 0)
        self._total_size -= size

    def _remove_no_lock(self, key: Path) -> None:
        if key in self._cache:
            self._cache.pop(key, None)
            size = self._sizes.pop(key, 0)
            self._total_size -= size

    def _estimate_size(self, obj: Any) -> int:
        # Approximate deep size to guide eviction decisions.
        seen: set[int] = set()

        def sizeof(o: Any) -> int:
            oid = id(o)
            if oid in seen:
                return 0
            seen.add(oid)
            try:
                size = sys.getsizeof(o)
            except Exception:
                size = 0

            if isinstance(o, dict):
                for k, v in o.items():
                    size += sizeof(k)
                    size += sizeof(v)
            elif isinstance(o, (list, tuple, set, frozenset)):
                for i in o:
                    size += sizeof(i)
            else:
                # Traverse object attributes if available
                if hasattr(o, "__dict__"):
                    size += sizeof(vars(o))
                # Handle slots
                slots = getattr(type(o), "__slots__", ())
                if isinstance(slots, (tuple, list)):
                    for s in slots:
                        try:
                            size += sizeof(getattr(o, s))
                        except Exception:
                            pass
            return size

        return sizeof(obj)
