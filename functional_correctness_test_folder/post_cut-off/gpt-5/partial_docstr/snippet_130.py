from __future__ import annotations

import pickle
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Any

try:
    from libcst import CSTNode as Node  # type: ignore
except Exception:
    from typing import Any as Node  # type: ignore


class BoundedASTCache:
    def __init__(self, max_entries: int = 1000, max_memory_mb: int = 500):
        self._cache: OrderedDict[Path, tuple[Node, str]] = OrderedDict()
        self._sizes: dict[Path, int] = {}
        self._memory_bytes: int = 0
        self._max_entries = int(max(0, max_entries))
        self._max_memory_bytes = int(max(0, max_memory_mb)) * 1024 * 1024

    def __setitem__(self, key: Path, value: tuple[Node, str]) -> None:
        if key in self._cache:
            self.__delitem__(key)
        size = self._estimate_entry_size(key, value)
        self._cache[key] = value
        self._sizes[key] = size
        self._memory_bytes += size
        self._cache.move_to_end(key, last=True)
        self._enforce_limits()

    def __getitem__(self, key: Path) -> tuple[Node, str]:
        value = self._cache[key]
        self._cache.move_to_end(key, last=True)
        return value

    def __delitem__(self, key: Path) -> None:
        if key in self._cache:
            self._memory_bytes -= self._sizes.get(key, 0)
            self._sizes.pop(key, None)
            del self._cache[key]

    def __contains__(self, key: Path) -> bool:
        return key in self._cache

    def items(self) -> Any:
        return self._cache.items()

    def _enforce_limits(self) -> None:
        while (self._max_entries and len(self._cache) > self._max_entries) or self._should_evict_for_memory():
            k, _ = self._cache.popitem(last=False)
            self._memory_bytes -= self._sizes.get(k, 0)
            self._sizes.pop(k, None)

    def _should_evict_for_memory(self) -> bool:
        return self._max_memory_bytes > 0 and self._memory_bytes > self._max_memory_bytes

    def _estimate_entry_size(self, key: Path, value: tuple[Node, str]) -> int:
        node, src = value
        size = 0

        # Key size (path)
        try:
            key_str = str(key)
            size += sys.getsizeof(key) + sys.getsizeof(key_str) + \
                len(key_str.encode("utf-8"))
        except Exception:
            size += sys.getsizeof(key)

        # Source string size
        try:
            src_bytes = src.encode("utf-8", errors="ignore")
            size += sys.getsizeof(src) + len(src_bytes)
        except Exception:
            size += sys.getsizeof(src)

        # Node size: try pickle, fallback to shallow sizeof
        try:
            node_bytes = pickle.dumps(node, protocol=pickle.HIGHEST_PROTOCOL)
            size += len(node_bytes)
        except Exception:
            size += sys.getsizeof(node)

        # Tuple/container overhead
        size += sys.getsizeof(value)
        return int(size)
