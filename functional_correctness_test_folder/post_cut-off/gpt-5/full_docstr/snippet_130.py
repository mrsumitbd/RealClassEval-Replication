from __future__ import annotations
import types  # placed here to avoid circular issues in the helper above

import sys
import threading
import gc
from collections import OrderedDict
from pathlib import Path
from typing import Any, ItemsView, Dict, Tuple

try:
    from ast import AST as Node  # type: ignore
except Exception:  # pragma: no cover
    Node = Any  # type: ignore


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
        if max_entries <= 0:
            raise ValueError("max_entries must be positive")
        if max_memory_mb <= 0:
            raise ValueError("max_memory_mb must be positive")

        self._max_entries = int(max_entries)
        self._max_memory_bytes = int(max_memory_mb) * 1024 * 1024

        self._cache: "OrderedDict[Path, Tuple[Node, str]]" = OrderedDict()
        self._sizes: Dict[Path, int] = {}
        self._total_bytes: int = 0

        self._lock = threading.RLock()

    def __setitem__(self, key: Path, value: tuple[Node, str]) -> None:
        '''Add or update an AST cache entry with automatic cleanup.'''
        if not isinstance(key, Path):
            key = Path(key)  # type: ignore[arg-type]

        with self._lock:
            # remove old if exists
            if key in self._cache:
                self._evict_key(key)

            size_bytes = self._estimate_size(value)
            self._cache[key] = value
            self._cache.move_to_end(key, last=True)
            self._sizes[key] = size_bytes
            self._total_bytes += size_bytes

            self._enforce_limits()

    def __getitem__(self, key: Path) -> tuple[Node, str]:
        '''Get AST cache entry and mark as recently used.'''
        if not isinstance(key, Path):
            key = Path(key)  # type: ignore[arg-type]

        with self._lock:
            value = self._cache[key]
            self._cache.move_to_end(key, last=True)
            return value

    def __delitem__(self, key: Path) -> None:
        '''Remove entry from cache.'''
        if not isinstance(key, Path):
            key = Path(key)  # type: ignore[arg-type]

        with self._lock:
            self._evict_key(key)

    def __contains__(self, key: Path) -> bool:
        '''Check if key exists in cache.'''
        if not isinstance(key, Path):
            key = Path(key)  # type: ignore[arg-type]
        with self._lock:
            return key in self._cache

    def items(self) -> Any:
        '''Return all cache items'''
        with self._lock:
            # Return a snapshot to avoid race conditions on iteration
            return list(self._cache.items())

    def _enforce_limits(self) -> None:
        '''Enforce cache size and memory limits by evicting old entries.'''
        with self._lock:
            # Evict by entry count
            while len(self._cache) > self._max_entries:
                self._pop_lru()

            # Evict by memory pressure
            # loop in case large entries need multiple pops
            while self._should_evict_for_memory() and self._cache:
                self._pop_lru()

    def _should_evict_for_memory(self) -> bool:
        '''Check if we should evict entries due to memory pressure.'''
        with self._lock:
            return self._total_bytes > self._max_memory_bytes

    # Internal helpers

    def _pop_lru(self) -> None:
        key, _ = self._cache.popitem(last=False)
        size = self._sizes.pop(key, 0)
        self._total_bytes -= size
        if self._total_bytes < 0:
            self._total_bytes = 0

    def _evict_key(self, key: Path) -> None:
        if key in self._cache:
            self._cache.pop(key, None)
            size = self._sizes.pop(key, 0)
            self._total_bytes -= size
            if self._total_bytes < 0:
                self._total_bytes = 0

    def _estimate_size(self, obj: Any) -> int:
        # Recursive size estimation with cycle protection
        seen: set[int] = set()
        return self._recursive_size(obj, seen)

    def _recursive_size(self, obj: Any, seen: set[int]) -> int:
        obj_id = id(obj)
        if obj_id in seen:
            return 0
        seen.add(obj_id)

        size = sys.getsizeof(obj, 0)

        # Handle common containers and AST-like objects
        if isinstance(obj, dict):
            for k, v in obj.items():
                size += self._recursive_size(k, seen)
                size += self._recursive_size(v, seen)
            return size

        if isinstance(obj, (list, tuple, set, frozenset)):
            for item in obj:
                size += self._recursive_size(item, seen)
            return size

        # For AST nodes or generic objects: traverse __dict__ and slots if present
        # Avoid deep traversal of builtins like str/bytes/ints which are already accounted for
        if hasattr(obj, "__dict__"):
            size += self._recursive_size(vars(obj), seen)

        # Handle __slots__ if defined
        slots = getattr(obj, "__slots__", ())
        if slots:
            if isinstance(slots, str):
                slots = (slots,)
            for slot in slots:
                try:
                    attr = getattr(obj, slot)
                except Exception:
                    continue
                size += self._recursive_size(attr, seen)

        # Include referents for completeness but filter builtins for performance
        try:
            referents = [r for r in gc.get_referents(obj) if not isinstance(
                r, (type, types.ModuleType))]  # type: ignore
        except Exception:
            referents = []

        # Limit potential double counting by skipping dict/list/tuple already handled
        for r in referents:
            if isinstance(r, (dict, list, tuple, set, frozenset)):
                continue
            # basic immutables are already measured by getsizeof at top-level
            if isinstance(r, (str, bytes, bytearray, int, float, bool)):
                continue
            rid = id(r)
            if rid not in seen:
                size += self._recursive_size(r, seen)

        return size


# Fallback for types in get_referents filter
