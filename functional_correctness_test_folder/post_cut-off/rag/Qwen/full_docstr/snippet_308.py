
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
        self.blobs: OrderedDict[str, bytes] = OrderedDict()
        self.metadata: Dict[str, Dict[str, Any]] = {}

    def _evict_if_needed(self) -> None:
        '''Evict oldest blobs if we've exceeded max_size.'''
        while len(self.blobs) > self.max_size:
            oldest_blob_id = next(iter(self.blobs))
            del self.blobs[oldest_blob_id]
            del self.metadata[oldest_blob_id]

    def save(self, data: bytes, meta: dict[str, Any]) -> str:
        '''Save binary data with metadata.'''
        blob_id = str(len(self.blobs))
        self.blobs[blob_id] = data
        self.metadata[blob_id] = meta
        self._evict_if_needed()
        return blob_id

    def load(self, blob_id: str) -> bytes:
        '''Load binary data by blob ID.'''
        return self.blobs[blob_id]

    def info(self, blob_id: str) -> dict[str, Any]:
        '''Get metadata for a blob.'''
        return self.metadata[blob_id]

    def delete(self, blob_id: str) -> None:
        '''Delete a blob and its metadata.'''
        del self.blobs[blob_id]
        del self.metadata[blob_id]
