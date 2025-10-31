
import uuid
from collections import OrderedDict
from typing import Any, Dict


class InMemoryBlobStore:
    '''In-memory blob storage for testing and short-lived scenarios.'''

    def __init__(self, max_size: int = 100):
        '''
        Initialize in-memory blob store.
        Args:
            max_size: Maximum number of blobs to keep in memory
        '''
        self.max_size = max_size
        # OrderedDict preserves insertion order; key -> (data, meta)
        self._store: "OrderedDict[str, tuple[bytes, dict[str, Any]]]" = OrderedDict(
        )

    def _evict_if_needed(self) -> None:
        '''Evict oldest blobs if we've exceeded max_size.'''
        while len(self._store) > self.max_size:
            # popitem(last=False) removes the first (oldest) item
            self._store.popitem(last=False)

    def save(self, data: bytes, meta: dict[str, Any]) -> str:
        '''Save binary data with metadata.'''
        blob_id = uuid.uuid4().hex
        self._store[blob_id] = (data, meta)
        self._evict_if_needed()
        return blob_id

    def load(self, blob_id: str) -> bytes:
        '''Load binary data by blob ID.'''
        try:
            data, _ = self._store[blob_id]
            return data
        except KeyError as exc:
            raise KeyError(f"Blob ID {blob_id!r} not found") from exc

    def info(self, blob_id: str) -> dict[str, Any]:
        '''Get metadata for a blob.'''
        try:
            _, meta = self._store[blob_id]
            return meta
        except KeyError as exc:
            raise KeyError(f"Blob ID {blob_id!r} not found") from exc

    def delete(self, blob_id: str) -> None:
        '''Delete a blob and its metadata.'''
        try:
            del self._store[blob_id]
        except KeyError as exc:
            raise KeyError(f"Blob ID {blob_id!r} not found") from exc
