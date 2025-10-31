from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

import sys


Node = Any


@dataclass
class _Entry:
    value: tuple[Node, str]
    size_bytes: int


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
        from threading import RLock

        self._max_entries = int(max_entries) if max_entries > 0 else 1
        self._max_memory_bytes = int(
            max_memory_mb) * 1024 * 1024 if max_memory_mb > 0 else 0
        self._cache: OrderedDict[Path, _Entry] = OrderedDict()
        self._current_bytes = 0
        self._lock = RLock()

    def __setitem__(self, key: Path, value: tuple[Node, str]) -> None:
        '''Add or update an AST cache entry with automatic cleanup.'''
        if not isinstance(key, Path):
            raise TypeError('Key must be a pathlib.Path')
        if not (isinstance(value, tuple) and len(value) == 2):
            raise TypeError('Value must be a tuple[Node, str]')
        if not isinstance(value[1], str):
            raise TypeError('Second element of value must be str')

        size = self._estimate_entry_size(value)
        with self._lock:
            if key in self._cache:
                old = self._cache.pop(key)
                self._current_bytes -= old.size_bytes
            self._cache[key] = _Entry(value=value, size_bytes=size)
            self._current_bytes += size
            self._cache.move_to_end(key, last=True)
            self._enforce_limits()

    def __getitem__(self, key: Path) -> tuple[Node, str]:
        '''Get AST cache entry and mark as recently used.'''
        with self._lock:
            entry = self._cache[key]
            # mark as recently used
            self._cache.move_to_end(key, last=True)
            return entry.value

    def __delitem__(self, key: Path) -> None:
        '''Remove entry from cache.'''
        with self._lock:
            entry = self._cache.pop(key)
            self._current_bytes -= entry.size_bytes
            if self._current_bytes < 0:
                self._current_bytes = 0

    def __contains__(self, key: Path) -> bool:
        '''Check if key exists in cache.'''
        with self._lock:
            return key in self._cache

    def items(self) -> Any:
        '''Return all cache items.'''
        with self._lock:
            return [(k, v.value) for k, v in self._cache.items()]

    def _enforce_limits(self) -> None:
        '''Enforce cache size and memory limits by evicting old entries.'''
        with self._lock:
            # Enforce entry count
            while len(self._cache) > self._max_entries:
                k, v = self._cache.popitem(last=False)
                self._current_bytes -= v.size_bytes
            # Enforce memory usage
            # Allow one oversized entry to remain to avoid infinite eviction loop
            while self._should_evict_for_memory() and len(self._cache) > 1:
                k, v = self._cache.popitem(last=False)
                self._current_bytes -= v.size_bytes
            if self._current_bytes < 0:
                self._current_bytes = 0

    def _should_evict_for_memory(self) -> bool:
        '''Check if we should evict entries due to memory pressure.'''
        if self._max_memory_bytes <= 0:
            return False
        return self._current_bytes > self._max_memory_bytes

    def _estimate_entry_size(self, value: tuple[Node, str]) -> int:
        # Heuristic: size of associated source string + estimated AST size.
        size = 0
        try:
            size += len(value[1].encode('utf-8'))
        except Exception:
            size += len(value[1]) if isinstance(value[1], str) else 0

        # Estimate AST object size with bounded deep traversal
        seen: set[int] = set()
        max_depth = 3

        def deep_size(obj: Any, depth: int) -> int:
            oid = id(obj)
            if oid in seen:
                return 0
            seen.add(oid)
            try:
                base = sys.getsizeof(obj)
            except Exception:
                base = 0
            if depth <= 0:
                return base
            # Do not expand across common atomic types
            if isinstance(obj, (str, bytes, bytearray, memoryview, int, float, bool, type(None))):
                return base
            subtotal = base
            if isinstance(obj, dict):
                for k, v in obj.items():
                    subtotal += deep_size(k, depth - 1)
                    subtotal += deep_size(v, depth - 1)
                return subtotal
            # Handle objects with __dict__ or __slots__
            if hasattr(obj, '__dict__'):
                subtotal += deep_size(vars(obj), depth - 1)
            if hasattr(obj, '__slots__'):
                for attr in getattr(obj, '__slots__', ()):
                    try:
                        slot_val = getattr(obj, attr)
                    except Exception:
                        continue
                    subtotal += deep_size(slot_val, depth - 1)
            # Generic iterables
            try:
                from collections.abc import Mapping, Iterable as It
                if isinstance(obj, It) and not isinstance(obj, (str, bytes, bytearray, memoryview)):
                    for item in obj:
                        subtotal += deep_size(item, depth - 1)
            except Exception:
                pass
            return subtotal

        try:
            size += deep_size(value[0], max_depth)
        except Exception:
            # Fallback fixed overhead if AST cannot be traversed
            size += 64 * 1024  # 64 KiB as conservative fallback

        # Ensure non-negative integer
        return int(max(size, 0))
