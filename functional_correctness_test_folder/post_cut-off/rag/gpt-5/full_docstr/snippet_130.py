from __future__ import annotations

import threading
from collections import OrderedDict
from pathlib import Path
from typing import Any, Iterator, Tuple

try:
    # Prefer Python's ast.AST as a reasonable "Node" placeholder for typing.
    from ast import AST as Node  # type: ignore[assignment]
except Exception:
    # Fallback typing alias
    class Node:  # type: ignore[override]
        pass

try:
    import psutil  # type: ignore
except Exception:  # pragma: no cover
    psutil = None  # type: ignore


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
        self._lock = threading.RLock()
        self._data: "OrderedDict[Path, tuple[tuple[Node, str], int]]" = OrderedDict(
        )
        self._max_entries = int(max(0, max_entries))
        self._max_memory_mb = int(max(0, max_memory_mb))
        self._total_size_bytes = 0

    def __setitem__(self, key: Path, value: tuple[Node, str]) -> None:
        '''Add or update an AST cache entry with automatic cleanup.'''
        with self._lock:
            size = self._estimate_size(value)
            if key in self._data:
                _, old_size = self._data.pop(key)
                self._total_size_bytes -= old_size
            self._data[key] = (value, size)
            self._total_size_bytes += size
            self._data.move_to_end(key, last=True)
            self._enforce_limits()

    def __getitem__(self, key: Path) -> tuple[Node, str]:
        '''Get AST cache entry and mark as recently used.'''
        with self._lock:
            value_size = self._data[key]
            # Touch LRU
            self._data.move_to_end(key, last=True)
            return value_size[0]

    def __delitem__(self, key: Path) -> None:
        '''Remove entry from cache.'''
        with self._lock:
            _, size = self._data.pop(key)
            self._total_size_bytes -= size

    def __contains__(self, key: Path) -> bool:
        '''Check if key exists in cache.'''
        with self._lock:
            return key in self._data

    def items(self) -> Iterator[tuple[Path, tuple[Node, str]]]:
        '''Return all cache items.'''
        with self._lock:
            # Snapshot to avoid holding lock during iteration by caller
            snapshot = list(self._data.items())
        for k, (v, _) in snapshot:
            yield k, v

    def _enforce_limits(self) -> None:
        '''Enforce cache size and memory limits by evicting old entries.'''
        with self._lock:
            # Evict by entry count first
            while self._max_entries and len(self._data) > self._max_entries:
                k, (_, size) = self._data.popitem(last=False)
                self._total_size_bytes -= size
            # Evict by memory pressure
            while self._should_evict_for_memory() and self._data:
                k, (_, size) = self._data.popitem(last=False)
                self._total_size_bytes -= size

    def _should_evict_for_memory(self) -> bool:
        '''Check if we should evict entries due to memory pressure.'''
        if not self._max_memory_mb:
            return False
        cache_mb = self._total_size_bytes / (1024 * 1024)
        if cache_mb > self._max_memory_mb:
            return True
        if psutil is not None:
            try:
                proc = psutil.Process()
                rss_mb = proc.memory_info().rss / (1024 * 1024)
                if rss_mb > self._max_memory_mb:
                    return True
            except Exception:
                # If psutil fails, fall back to cache-based decision only
                pass
        return False

    def _estimate_size(self, value: tuple[Node, str]) -> int:
        # Estimate deep size of the cached tuple
        seen: set[int] = set()
        try:
            return self._deep_getsizeof(value, seen)
        except Exception:
            # Fallback minimal estimate: size of tuple + sizes of direct members
            import sys
            try:
                return (
                    sys.getsizeof(value)
                    + sys.getsizeof(value[0])
                    + sys.getsizeof(value[1])
                )
            except Exception:
                return 0

    def _deep_getsizeof(self, obj: Any, seen: set[int]) -> int:
        import sys

        obj_id = id(obj)
        if obj_id in seen:
            return 0
        seen.add(obj_id)

        size = sys.getsizeof(obj)

        if isinstance(obj, dict):
            for k, v in obj.items():
                size += self._deep_getsizeof(k, seen)
                size += self._deep_getsizeof(v, seen)
            return size

        if isinstance(obj, (list, tuple, set, frozenset)):
            for item in obj:
                size += self._deep_getsizeof(item, seen)
            return size

        # Include __dict__ contents
        if hasattr(obj, "__dict__"):
            try:
                size += self._deep_getsizeof(vars(obj), seen)
            except Exception:
                pass

        # Include __slots__ contents
        slots = getattr(obj.__class__, "__slots__", None)
        if slots:
            if isinstance(slots, str):
                slots = [slots]
            for s in slots:
                try:
                    size += self._deep_getsizeof(getattr(obj, s), seen)
                except Exception:
                    pass

        return size
