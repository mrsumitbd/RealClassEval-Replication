from __future__ import annotations

from typing import Any, Dict
from collections import OrderedDict
from threading import RLock
import uuid
import time
import copy


class InMemoryBlobStore:
    def __init__(self, max_size: int = 100):
        if not isinstance(max_size, int):
            raise TypeError("max_size must be an int")
        if max_size < 0:
            raise ValueError("max_size must be >= 0")
        self._max_size: int = max_size
        self._store: "OrderedDict[str, Dict[str, Any]]" = OrderedDict()
        self._lock = RLock()

    def _evict_if_needed(self) -> None:
        '''Evict oldest blobs if we've exceeded max_size.'''
        with self._lock:
            while len(self._store) > self._max_size:
                self._store.popitem(last=False)

    def save(self, data: bytes, meta: dict[str, Any]) -> str:
        '''Save binary data with metadata.'''
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise TypeError("data must be bytes-like")
        if not isinstance(meta, dict):
            raise TypeError("meta must be a dict[str, Any]")
        blob_id = uuid.uuid4().hex
        with self._lock:
            # copy meta to avoid external mutation
            meta_copy = copy.deepcopy(meta)
            self._store[blob_id] = {
                "data": bytes(data),
                "meta": meta_copy,
                "created_at": time.time(),
            }
            # Maintain insertion order: ensure new item is considered newest
            self._store.move_to_end(blob_id, last=True)
            self._evict_if_needed()
        return blob_id

    def load(self, blob_id: str) -> bytes:
        with self._lock:
            if blob_id not in self._store:
                raise KeyError(f"blob_id not found: {blob_id}")
            return self._store[blob_id]["data"]

    def info(self, blob_id: str) -> dict[str, Any]:
        '''Get metadata for a blob.'''
        with self._lock:
            if blob_id not in self._store:
                raise KeyError(f"blob_id not found: {blob_id}")
            # Return a copy to prevent external mutation
            return copy.deepcopy(self._store[blob_id]["meta"])

    def delete(self, blob_id: str) -> None:
        with self._lock:
            if blob_id not in self._store:
                raise KeyError(f"blob_id not found: {blob_id}")
            del self._store[blob_id]
