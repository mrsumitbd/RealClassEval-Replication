
from __future__ import annotations

from pathlib import Path
from collections import OrderedDict
import sys
import ast
from typing import Any, Tuple, Dict, Iterator


class BoundedASTCache:
    """
    A bounded cache for storing AST nodes and their source code.
    The cache evicts the least‑recently‑used items when either the
    maximum number of entries or the maximum memory usage is exceeded.
    """

    def __init__(self, max_entries: int = 1000, max_memory_mb: int = 500):
        self.max_entries = max_entries
        self.max_memory_mb = max_memory_mb
        self._store: "OrderedDict[Path, Tuple[ast.AST, str]]" = OrderedDict()
        self._current_memory: int = 0  # in bytes

    # ------------------------------------------------------------------
    # Public mapping interface
    # ------------------------------------------------------------------
    def __setitem__(self, key: Path, value: Tuple[ast.AST, str]) -> None:
        """Insert or update an entry and enforce size limits."""
        # If key already exists, remove old entry first
        if key in self._store:
            self.__delitem__(key)

        # Estimate memory usage of the new entry
        entry_size = sys.getsizeof(
            key) + sys.getsizeof(value[0]) + sys.getsizeof(value[1])
        self._store[key] = value
        self._current_memory += entry_size

        # Move to end to mark as most recently used
        self._store.move_to_end(key)

        self._enforce_limits()

    def __getitem__(self, key: Path) -> Tuple[ast.AST, str]:
        """Retrieve an entry and mark it as recently used."""
        if key not in self._store:
            raise KeyError(key)
        value = self._store[key]
        self._store.move_to_end(key)
        return value

    def __delitem__(self, key: Path) -> None:
        """Remove an entry and adjust memory counter."""
        if key not in self._store:
            raise KeyError(key)
        value = self._store.pop(key)
        entry_size = sys.getsizeof(
            key) + sys.getsizeof(value[0]) + sys.getsizeof(value[1])
        self._current_memory -= entry_size

    def __contains__(self, key: Path) -> bool:
        return key in self._store

    def items(self) -> Iterator[Tuple[Path, Tuple[ast.AST, str]]]:
        """Return an iterator over the cache items."""
        return iter(self._store.items())

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _enforce_limits(self) -> None:
        """Evict entries until both limits are satisfied."""
        while (
            len(self._store) > self.max_entries
            or self._should_evict_for_memory()
        ):
            # Evict the least‑recently‑used item (first item in OrderedDict)
            key, value = self._store.popitem(last=False)
            entry_size = sys.getsizeof(
                key) + sys.getsizeof(value[0]) + sys.getsizeof(value[1])
            self._current_memory -= entry_size

    def _should_evict_for_memory(self) -> bool:
        """Return True if current memory usage exceeds the configured limit."""
        return self._current_memory > self.max_memory_mb * 1024 * 1024
