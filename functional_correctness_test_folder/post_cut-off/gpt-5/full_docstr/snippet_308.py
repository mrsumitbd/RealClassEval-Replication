from __future__ import annotations

from collections import OrderedDict
from threading import RLock
from typing import Any
import uuid
import time
import copy


class InMemoryBlobStore:
    '''In-memory blob storage for testing and short-lived scenarios.'''

    def __init__(self, max_size: int = 100):
        '''
        Initialize in-memory blob store.
        Args:
            max_size: Maximum number of blobs to keep in memory
        '''
        if not isinstance(max_size, int) or max_size <= 0:
            raise ValueError("max_size must be a positive integer")
        self._max_size = max_size
        self._store: OrderedDict[str,
                                 tuple[bytes, dict[str, Any]]] = OrderedDict()
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
            raise TypeError("meta must be a dict")

        with self._lock:
            blob_id = uuid.uuid4().hex
            # Normalize data to immutable bytes
            data_bytes = bytes(data)
            meta_copy = copy.deepcopy(meta)
            # Add basic metadata
            meta_copy.setdefault("created_at", time.time())
            meta_copy.setdefault("size", len(data_bytes))
            self._store[blob_id] = (data_bytes, meta_copy)
            # Maintain insertion order and capacity
            self._evict_if_needed()
            return blob_id

    def load(self, blob_id: str) -> bytes:
        '''Load binary data by blob ID.'''
        if not isinstance(blob_id, str):
            raise TypeError("blob_id must be a string")
        with self._lock:
            try:
                data, _ = self._store[blob_id]
            except KeyError as e:
                raise KeyError(f"Blob not found: {blob_id}") from e
            return data

    def info(self, blob_id: str) -> dict[str, Any]:
        '''Get metadata for a blob.'''
        if not isinstance(blob_id, str):
            raise TypeError("blob_id must be a string")
        with self._lock:
            try:
                _, meta = self._store[blob_id]
            except KeyError as e:
                raise KeyError(f"Blob not found: {blob_id}") from e
            return copy.deepcopy(meta)

    def delete(self, blob_id: str) -> None:
        '''Delete a blob and its metadata.'''
        if not isinstance(blob_id, str):
            raise TypeError("blob_id must be a string")
        with self._lock:
            try:
                del self._store[blob_id]
            except KeyError as e:
                raise KeyError(f"Blob not found: {blob_id}") from e
