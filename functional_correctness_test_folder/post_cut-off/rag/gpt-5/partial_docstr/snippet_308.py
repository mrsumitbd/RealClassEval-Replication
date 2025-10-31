from typing import Any
from collections import OrderedDict
from threading import RLock
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
        if max_size < 1:
            raise ValueError('max_size must be >= 1')
        self.max_size = int(max_size)
        self._store: OrderedDict[str,
                                 tuple[bytes, dict[str, Any]]] = OrderedDict()
        self._lock = RLock()

    def _evict_if_needed(self) -> None:
        '''Evict oldest blobs if we've exceeded max_size.'''
        with self._lock:
            while len(self._store) > self.max_size:
                self._store.popitem(last=False)

    def save(self, data: bytes, meta: dict[str, Any]) -> str:
        '''Save binary data with metadata.'''
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise TypeError('data must be bytes-like')
        if not isinstance(meta, dict):
            raise TypeError('meta must be a dict')

        blob_id = uuid.uuid4().hex
        with self._lock:
            while blob_id in self._store:
                blob_id = uuid.uuid4().hex
            # Store a copy of meta to prevent external mutation
            self._store[blob_id] = (bytes(data), copy.deepcopy(meta))
            self._evict_if_needed()
        return blob_id

    def load(self, blob_id: str) -> bytes:
        '''Load binary data by blob ID.'''
        with self._lock:
            try:
                data, _ = self._store[blob_id]
                return data
            except KeyError:
                raise KeyError(f'Blob not found: {blob_id}')

    def info(self, blob_id: str) -> dict[str, Any]:
        '''Get metadata for a blob.'''
        with self._lock:
            try:
                _, meta = self._store[blob_id]
                return copy.deepcopy(meta)
            except KeyError:
                raise KeyError(f'Blob not found: {blob_id}')

    def delete(self, blob_id: str) -> None:
        '''Delete a blob and its metadata.'''
        with self._lock:
            try:
                del self._store[blob_id]
            except KeyError:
                raise KeyError(f'Blob not found: {blob_id}')
