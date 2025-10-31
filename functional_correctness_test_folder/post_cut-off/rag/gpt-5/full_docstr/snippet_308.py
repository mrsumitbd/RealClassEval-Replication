from typing import Any, Dict, Optional
from collections import OrderedDict
from threading import RLock
import time
import uuid


class InMemoryBlobStore:
    '''In-memory blob storage for testing and short-lived scenarios.'''

    def __init__(self, max_size: int = 100):
        '''
        Initialize in-memory blob store.
        Args:
            max_size: Maximum number of blobs to keep in memory
        '''
        if not isinstance(max_size, int) or max_size < 0:
            raise ValueError('max_size must be a non-negative integer')
        self.max_size = max_size
        self._store: "OrderedDict[str, Dict[str, Any]]" = OrderedDict()
        self._lock = RLock()

    def _evict_if_needed(self) -> None:
        '''Evict oldest blobs if we've exceeded max_size.'''
        if self.max_size < 0:
            return
        while len(self._store) > self.max_size:
            self._store.popitem(last=False)

    def save(self, data: bytes, meta: dict[str, Any]) -> str:
        '''Save binary data with metadata.'''
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise TypeError('data must be bytes-like')
        if not isinstance(meta, dict):
            raise TypeError('meta must be a dict')

        # Ensure bytes type for storage
        bdata = bytes(data)

        record_meta = dict(meta)
        created_at = time.time()
        size = len(bdata)

        blob_id = uuid.uuid4().hex
        with self._lock:
            # Ensure extremely unlikely collision is handled
            while blob_id in self._store:
                blob_id = uuid.uuid4().hex
            self._store[blob_id] = {
                'data': bdata,
                'meta': record_meta,
                'created_at': created_at,
                'size': size,
            }
            self._evict_if_needed()
        return blob_id

    def load(self, blob_id: str) -> bytes:
        '''Load binary data by blob ID.'''
        with self._lock:
            record = self._store.get(blob_id)
            if record is None:
                raise KeyError(f'Blob not found: {blob_id}')
            return record['data']

    def info(self, blob_id: str) -> dict[str, Any]:
        '''Get metadata for a blob.'''
        with self._lock:
            record = self._store.get(blob_id)
            if record is None:
                raise KeyError(f'Blob not found: {blob_id}')
            # Return structured info to avoid key collisions
            return {
                'id': blob_id,
                'size': record['size'],
                'created_at': record['created_at'],
                'meta': dict(record['meta']),
            }

    def delete(self, blob_id: str) -> None:
        '''Delete a blob and its metadata.'''
        with self._lock:
            if blob_id not in self._store:
                raise KeyError(f'Blob not found: {blob_id}')
            del self._store[blob_id]
