from typing import Any, Dict
import uuid
from collections import OrderedDict


class InMemoryBlobStore:
    '''In-memory blob storage for testing and short-lived scenarios.'''

    def __init__(self, max_size: int = 100):
        '''
        Initialize in-memory blob store.
        Args:
            max_size: Maximum number of blobs to keep in memory
        '''
        self.max_size = max_size
        self._blobs: "OrderedDict[str, tuple[bytes, dict[str, Any]]]" = OrderedDict(
        )

    def _evict_if_needed(self) -> None:
        '''Evict oldest blobs if we've exceeded max_size.'''
        while len(self._blobs) > self.max_size:
            self._blobs.popitem(last=False)

    def save(self, data: bytes, meta: dict[str, Any]) -> str:
        '''Save binary data with metadata.'''
        blob_id = str(uuid.uuid4())
        self._blobs[blob_id] = (data, dict(meta))
        self._evict_if_needed()
        return blob_id

    def load(self, blob_id: str) -> bytes:
        '''Load binary data by blob ID.'''
        if blob_id not in self._blobs:
            raise KeyError(f"Blob ID {blob_id} not found")
        return self._blobs[blob_id][0]

    def info(self, blob_id: str) -> dict[str, Any]:
        '''Get metadata for a blob.'''
        if blob_id not in self._blobs:
            raise KeyError(f"Blob ID {blob_id} not found")
        return dict(self._blobs[blob_id][1])

    def delete(self, blob_id: str) -> None:
        '''Delete a blob and its metadata.'''
        if blob_id in self._blobs:
            del self._blobs[blob_id]
        else:
            raise KeyError(f"Blob ID {blob_id} not found")
