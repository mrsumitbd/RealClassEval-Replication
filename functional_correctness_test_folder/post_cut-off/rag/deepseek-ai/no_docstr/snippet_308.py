
from typing import Dict, Any, OrderedDict
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
        self.blobs: OrderedDict[str, bytes] = OrderedDict()
        self.metadata: Dict[str, Dict[str, Any]] = {}

    def _evict_if_needed(self) -> None:
        '''Evict oldest blobs if we've exceeded max_size.'''
        while len(self.blobs) > self.max_size:
            blob_id, _ = self.blobs.popitem(last=False)
            del self.metadata[blob_id]

    def save(self, data: bytes, meta: Dict[str, Any]) -> str:
        '''Save binary data with metadata.'''
        blob_id = str(uuid.uuid4())
        self.blobs[blob_id] = data
        self.metadata[blob_id] = meta
        self._evict_if_needed()
        return blob_id

    def load(self, blob_id: str) -> bytes:
        '''Load binary data by blob ID.'''
        if blob_id not in self.blobs:
            raise KeyError(f"Blob ID {blob_id} not found")
        # Move to end to mark as recently used
        data = self.blobs.pop(blob_id)
        self.blobs[blob_id] = data
        return data

    def info(self, blob_id: str) -> Dict[str, Any]:
        '''Get metadata for a blob.'''
        if blob_id not in self.metadata:
            raise KeyError(f"Blob ID {blob_id} not found")
        return self.metadata[blob_id]

    def delete(self, blob_id: str) -> None:
        '''Delete a blob and its metadata.'''
        if blob_id in self.blobs:
            del self.blobs[blob_id]
        if blob_id in self.metadata:
            del self.metadata[blob_id]
