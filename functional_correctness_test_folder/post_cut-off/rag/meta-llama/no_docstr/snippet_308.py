
from typing import Any, Dict
from collections import OrderedDict
import uuid


class InMemoryBlobStore:
    """In-memory blob storage for testing and short-lived scenarios."""

    def __init__(self, max_size: int = 100):
        """
        Initialize in-memory blob store.

        Args:
            max_size: Maximum number of blobs to keep in memory
        """
        self.max_size = max_size
        self.blob_store: Dict[str, Dict[str, Any]] = {}
        self.blob_order: OrderedDict[str, None] = OrderedDict()

    def _evict_if_needed(self) -> None:
        """Evict oldest blobs if we've exceeded max_size."""
        while len(self.blob_store) > self.max_size:
            oldest_blob_id = next(iter(self.blob_order))
            del self.blob_store[oldest_blob_id]
            del self.blob_order[oldest_blob_id]

    def save(self, data: bytes, meta: Dict[str, Any]) -> str:
        """Save binary data with metadata."""
        blob_id = str(uuid.uuid4())
        self.blob_store[blob_id] = {'data': data, 'meta': meta}
        self.blob_order[blob_id] = None
        self._evict_if_needed()
        return blob_id

    def load(self, blob_id: str) -> bytes:
        """Load binary data by blob ID."""
        if blob_id not in self.blob_store:
            raise KeyError(f'Blob {blob_id} not found')
        self.blob_order.move_to_end(blob_id)
        return self.blob_store[blob_id]['data']

    def info(self, blob_id: str) -> Dict[str, Any]:
        """Get metadata for a blob."""
        if blob_id not in self.blob_store:
            raise KeyError(f'Blob {blob_id} not found')
        return self.blob_store[blob_id]['meta']

    def delete(self, blob_id: str) -> None:
        """Delete a blob and its metadata."""
        if blob_id in self.blob_store:
            del self.blob_store[blob_id]
            del self.blob_order[blob_id]
