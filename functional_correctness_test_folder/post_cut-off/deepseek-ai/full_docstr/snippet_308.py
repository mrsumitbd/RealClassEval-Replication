
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
        self.blobs_data: Dict[str, bytes] = OrderedDict()
        self.blobs_meta: Dict[str, Dict[str, Any]] = OrderedDict()

    def _evict_if_needed(self) -> None:
        '''Evict oldest blobs if we've exceeded max_size.'''
        while len(self.blobs_data) > self.max_size:
            oldest_blob_id = next(iter(self.blobs_data))
            del self.blobs_data[oldest_blob_id]
            del self.blobs_meta[oldest_blob_id]

    def save(self, data: bytes, meta: Dict[str, Any]) -> str:
        '''Save binary data with metadata.'''
        blob_id = str(uuid.uuid4())
        self.blobs_data[blob_id] = data
        self.blobs_meta[blob_id] = meta
        self._evict_if_needed()
        return blob_id

    def load(self, blob_id: str) -> bytes:
        '''Load binary data by blob ID.'''
        if blob_id not in self.blobs_data:
            raise KeyError(f"Blob ID {blob_id} not found")
        return self.blobs_data[blob_id]

    def info(self, blob_id: str) -> Dict[str, Any]:
        '''Get metadata for a blob.'''
        if blob_id not in self.blobs_meta:
            raise KeyError(f"Blob ID {blob_id} not found")
        return self.blobs_meta[blob_id]

    def delete(self, blob_id: str) -> None:
        '''Delete a blob and its metadata.'''
        if blob_id in self.blobs_data:
            del self.blobs_data[blob_id]
        if blob_id in self.blobs_meta:
            del self.blobs_meta[blob_id]
