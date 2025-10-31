
import uuid
from typing import Any, Dict, List, Tuple


class InMemoryBlobStore:
    '''In-memory blob storage for testing and short-lived scenarios.'''

    def __init__(self, max_size: int = 100):
        '''
        Initialize in-memory blob store.
        Args:
            max_size: Maximum number of blobs to keep in memory
        '''
        self.max_size = max_size
        self.blobs: Dict[str, bytes] = {}
        self.meta: Dict[str, Dict[str, Any]] = {}
        self.access_order: List[str] = []

    def _evict_if_needed(self) -> None:
        '''Evict oldest blobs if we've exceeded max_size.'''
        while len(self.blobs) > self.max_size:
            oldest_blob_id = self.access_order.pop(0)
            del self.blobs[oldest_blob_id]
            del self.meta[oldest_blob_id]

    def save(self, data: bytes, meta: dict[str, Any]) -> str:
        '''Save binary data with metadata.'''
        blob_id = str(uuid.uuid4())
        self.blobs[blob_id] = data
        self.meta[blob_id] = meta
        self.access_order.append(blob_id)
        self._evict_if_needed()
        return blob_id

    def load(self, blob_id: str) -> bytes:
        '''Load binary data by blob ID.'''
        if blob_id in self.blobs:
            self.access_order.remove(blob_id)
            self.access_order.append(blob_id)
            return self.blobs[blob_id]
        raise KeyError(f"Blob ID {blob_id} not found")

    def info(self, blob_id: str) -> dict[str, Any]:
        '''Get metadata for a blob.'''
        if blob_id in self.meta:
            self.access_order.remove(blob_id)
            self.access_order.append(blob_id)
            return self.meta[blob_id]
        raise KeyError(f"Blob ID {blob_id} not found")

    def delete(self, blob_id: str) -> None:
        '''Delete a blob and its metadata.'''
        if blob_id in self.blobs:
            self.access_order.remove(blob_id)
            del self.blobs[blob_id]
            del self.meta[blob_id]
        else:
            raise KeyError(f"Blob ID {blob_id} not found")
