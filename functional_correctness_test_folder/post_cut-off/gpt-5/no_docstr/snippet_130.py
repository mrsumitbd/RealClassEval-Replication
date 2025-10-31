from __future__ import annotations

import sys
from collections import OrderedDict
from pathlib import Path
from typing import Any, Iterator, MutableMapping, Tuple
from ast import AST as Node


class BoundedASTCache:
    def __init__(self, max_entries: int = 1000, max_memory_mb: int = 500):
        self._cache: "OrderedDict[Path, tuple[Node, str]]" = OrderedDict()
        self._sizes: "dict[Path, int]" = {}
        self._current_mem_bytes: int = 0
        self.max_entries = int(max_entries)
        self.max_memory_bytes = int(max_memory_mb) * 1024 * 1024

    def __setitem__(self, key: Path, value: tuple[Node, str]) -> None:
        if not isinstance(key, Path):
            raise TypeError("Key must be a pathlib.Path")
        # Compute size for new value
        new_size = self._deep_getsizeof(value)
        # If key exists, remove current to update size and recency
        if key in self._cache:
            self.__delitem__(key)
        # Insert new value at end (most recent)
        self._cache[key] = value
        self._sizes[key] = new_size
        self._current_mem_bytes += new_size
        # Enforce limits
        self._enforce_limits()

    def __getitem__(self, key: Path) -> tuple[Node, str]:
        value = self._cache[key]  # raises KeyError if not present
        # Move to end to mark as recently used
        self._cache.move_to_end(key)
        return value

    def __delitem__(self, key: Path) -> None:
        if key in self._cache:
            size = self._sizes.pop(key, 0)
            self._current_mem_bytes -= size
            if self._current_mem_bytes < 0:
                self._current_mem_bytes = 0
            del self._cache[key]
        else:
            raise KeyError(key)

    def __contains__(self, key: Path) -> bool:
        return key in self._cache

    def items(self) -> Iterator[tuple[Path, tuple[Node, str]]]:
        return iter(self._cache.items())

    def _enforce_limits(self) -> None:
        # Evict by count first
        while len(self._cache) > self.max_entries:
            self._evict_one()
        # Evict by memory while possible
        # Stop if eviction would empty cache or cannot reduce below limit due to single oversized item
        while self._should_evict_for_memory():
            if not self._cache:
                break
            if len(self._cache) == 1:
                # If single item exceeds memory limit, keep it to avoid infinite loop
                break
            self._evict_one()

    def _should_evict_for_memory(self) -> bool:
        return self._current_mem_bytes > self.max_memory_bytes

    def _evict_one(self) -> None:
        if not self._cache:
            return
        key, _ = self._cache.popitem(last=False)  # LRU eviction
        size = self._sizes.pop(key, 0)
        self._current_mem_bytes -= size
        if self._current_mem_bytes < 0:
            self._current_mem_bytes = 0

    def _deep_getsizeof(self, obj: Any, seen: set[int] | None = None) -> int:
        if seen is None:
            seen = set()
        obj_id = id(obj)
        if obj_id in seen:
            return 0
        seen.add(obj_id)

        size = sys.getsizeof(obj)

        # Handle AST nodes specially: traverse _fields if available
        if isinstance(obj, Node):
            for field in getattr(obj, "_fields", ()):
                try:
                    val = getattr(obj, field)
                except Exception:
                    continue
                size += self._deep_getsizeof(val, seen)
            # Also consider attributes stored elsewhere
            d = getattr(obj, "__dict__", None)
            if d:
                size += self._deep_getsizeof(d, seen)
            return size

        # Containers
        if isinstance(obj, dict):
            for k, v in obj.items():
                size += self._deep_getsizeof(k, seen)
                size += self._deep_getsizeof(v, seen)
            return size

        if isinstance(obj, (list, tuple, set, frozenset)):
            for item in obj:
                size += self._deep_getsizeof(item, seen)
            return size

        # Objects with __dict__
        d = getattr(obj, "__dict__", None)
        if d:
            size += self._deep_getsizeof(d, seen)

        # Objects with __slots__
        slots = getattr(type(obj), "__slots__", None)
        if slots:
            if isinstance(slots, str):
                slots = (slots,)
            for s in slots:
                if hasattr(obj, s):
                    try:
                        size += self._deep_getsizeof(getattr(obj, s), seen)
                    except Exception:
                        pass

        return size
