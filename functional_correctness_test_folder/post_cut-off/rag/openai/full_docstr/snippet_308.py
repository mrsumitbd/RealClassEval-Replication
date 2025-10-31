
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
        # OrderedDict preserves insertion order; keys are blob IDs
        self._blobs: OrderedDict[str, bytes] = OrderedDict()
        self._meta: Dict[str, Dict[str, Any]] = {}

    def _evict_if_needed(self) -> None:
        '''Evict oldest blobs if we've exceeded max_size.'''
        while len(self._blobs) > self.max_size:
            # popitem(last=False) pops the first (oldest) item
            blob_id, _ = self._blobs.popitem(last=False)
            self._meta.pop(blob_id, None)

    def save(self, data: bytes, meta: Dict[str, Any]) -> str:
        '''Save binary data with metadata.'''
        blob_id = str(uuid.uuid4())
        self._blobs[blob_id] = data
        self._meta[blob_id] = meta
        self._evict_if_needed()
        return blob_id

    def load(self, blob_id: str) -> bytes:
        '''Load binary data by blob ID.'''
        try:
            return self._blobs[blob_id]
        except KeyError as exc:
            raise KeyError(f'Blob ID {blob_id!r} not found') from exc

    def info(self, blob_id: str) -> Dict[str, Any]:
        '''Get metadata for a blob.'''
        try:
            return self._meta[blob_id]
        except KeyError as exc:
            raise KeyError(f'Blob ID {blob_id!r} not found') from exc

    def delete(self, blob_id: str) -> None:
        '''Delete a blob and its metadata.'''
        self._blobs.pop(blob_id, None)
        self._meta.pop(blob_id, None)
