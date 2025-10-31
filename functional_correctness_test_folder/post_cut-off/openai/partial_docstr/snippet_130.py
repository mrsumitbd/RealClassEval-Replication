
from __future__ import annotations

import sys
from collections import OrderedDict
from pathlib import Path
from typing import Any, Tuple

# The AST node type – we only need it for type hints.
try:
    from ast import AST as Node
except Exception:
    # Fallback if ast is not available – still works for type checking.
    class Node:  # pragma: no cover
        pass


class BoundedASTCache:
    """
    A bounded cache for storing AST nodes and their source code strings.
    The cache evicts the oldest entries when either the number of entries
    or the total memory usage exceeds the configured limits.
    """

    def __init__(self, max_entries: int = 1000, max_memory_mb: int = 500):
        """
        Parameters
        ----------
        max_entries : int
            Maximum number of entries the cache can hold.
        max_memory_mb : int
            Maximum memory usage in megabytes.
        """
        self._max_entries = max_entries
        self._max_memory_bytes = max_memory_mb * 1024 * 1024
        self._cache: OrderedDict[Path, Tuple[Node, str]] = OrderedDict()
        self._current_memory_bytes: int = 0

    def __setitem__(self, key: Path, value: Tuple[Node, str]) -> None:
        """
        Insert or update an entry in the cache.
        """
        # If key already exists, subtract its memory before replacing.
        if key in self._cache:
            old_node, old_src = self._cache[key]
            self._current_memory_bytes -= (
                sys.getsizeof(old_node) + sys.getsizeof(old_src)
            )

        self._cache[key] = value
        node, src = value
        self._current_memory_bytes += sys.getsizeof(node) + sys.getsizeof(src)

        # Move key to the end to mark it as most recently used.
        self._cache.move_to_end(key)

        self._enforce_limits()

    def __getitem__(self, key: Path) -> Tuple[Node, str]:
        """
        Retrieve an entry from the cache.
        """
        return self._cache[key]

    def __delitem__(self, key: Path) -> None:
        """
        Remove an entry from the cache.
        """
        node, src = self._cache.pop(key)
        self._current_memory_bytes -= sys.getsizeof(node) + sys.getsizeof(src)

    def __contains__(self, key: Path) -> bool:
        """
        Check if key exists in cache.
        """
        return key in self._cache

    def items(self) -> Any:
        """
        Return an iterator over the cache items.
        """
        return self._cache.items()

    def _enforce_limits(self) -> None:
        """
        Evict entries until the cache satisfies both size and memory limits.
        """
        # Evict based on entry count first.
        while len(self._cache) > self._max_entries:
            self._evict_oldest()

        # Then evict based on memory usage.
        while self._should_evict_for_memory():
            self._evict_oldest()

    def _should_evict_for_memory(self) -> bool:
        """
        Return True if the current memory usage exceeds the configured limit.
        """
        return self._current_memory_bytes > self._max_memory_bytes

    def _evict_oldest(self) -> None:
        """
        Remove the oldest entry from the cache.
        """
        key, (node, src) = self._cache.popitem(last=False)
        self._current_memory_bytes -= sys.getsizeof(node) + sys.getsizeof(src)
