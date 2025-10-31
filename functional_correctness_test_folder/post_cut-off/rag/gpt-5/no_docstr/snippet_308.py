from __future__ import annotations

from typing import Any
from collections import OrderedDict
import threading
import time
import uuid
import copy


class InMemoryBlobStore:
    '''In-memory blob storage for testing and short-lived scenarios.'''

    def __init__(self, max_size: int = 100):
        '''
        Initialize in-memory blob store.
        Args:
            max_size: Maximum number of blobs to keep in memory
        '''
        if max_size < 0:
            raise ValueError('max_size must be >= 0')
        self._max_size = int(max_size)
        self._store: OrderedDict[str, dict[str, Any]] = OrderedDict()
        self._lock = threading.RLock()

    def _evict_if_needed(self) -> None:
        '''Evict oldest blobs if we've exceeded max_size.'''
        with self._lock:
            while self._max_size >= 0 and len(self._store) > self._max_size:
                self._store.popitem(last=False)

    def save(self, data: bytes, meta: dict[str, Any]) -> str:
        '''Save binary data with metadata.'''
        if not isinstance(meta, dict):
            raise TypeError('meta must be a dict[str, Any]')
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise TypeError('data must be bytes-like')
        bdata = bytes(data)

        with self._lock:
            blob_id = uuid.uuid4().hex
            while blob_id in self._store:
                blob_id = uuid.uuid4().hex
            record = {
                'data': bdata,
                'meta': copy.deepcopy(meta),
                'created_at': time.time(),
                'size': len(bdata),
            }
            self._store[blob_id] = record
            self._evict_if_needed()
            return blob_id

    def load(self, blob_id: str) -> bytes:
        '''Load binary data by blob ID.'''
        with self._lock:
            try:
                return self._store[blob_id]['data']
            except KeyError:
                raise KeyError(f'Blob not found: {blob_id}') from None

    def info(self, blob_id: str) -> dict[str, Any]:
        '''Get metadata for a blob.'''
        with self._lock:
            try:
                rec = self._store[blob_id]
            except KeyError:
                raise KeyError(f'Blob not found: {blob_id}') from None
            # Combine system metadata with user metadata (user keys take precedence)
            info: dict[str, Any] = {
                'id': blob_id,
                'size': rec['size'],
                'created_at': rec['created_at'],
            }
            user_meta = copy.deepcopy(rec['meta'])
            info.update(user_meta)
            return info

    def delete(self, blob_id: str) -> None:
        '''Delete a blob and its metadata.'''
        with self._lock:
            try:
                del self._store[blob_id]
            except KeyError:
                raise KeyError(f'Blob not found: {blob_id}') from None
