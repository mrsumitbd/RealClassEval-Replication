
import time
from typing import Any, Dict, Optional
from collections import OrderedDict


class InMemoryBlobStore:
    """In-memory blob storage for testing and short-lived scenarios."""

    def __init__(self, max_size: int = 100):
        """
        Initialize in-memory blob store.
        Args:
            max_size: Maximum number of blobs to keep in memory
        """
        self.max_size = max_size
        self.blobs: OrderedDict[str, Dict[str, Any]] = OrderedDict()
        self.metadata: Dict[str, Dict[str, Any]] = {}

    def _evict_if_needed(self) -> None:
        """Evict oldest blobs if we've exceeded max_size."""
        while len(self.blobs) > self.max_size:
            blob_id, _ = self.blobs.popitem(last=False)
            self.metadata.pop(blob_id, None)

    def save(self, data: bytes, meta: Dict[str, Any]) -> str:
        """Save binary data with metadata."""
        blob_id = str(time.time_ns())
        self.blobs[blob_id] = {"data": data, "timestamp": time.time()}
        self.metadata[blob_id] = meta
        self._evict_if_needed()
        return blob_id

    def load(self, blob_id: str) -> bytes:
        """Load binary data by blob ID."""
        if blob_id not in self.blobs:
            raise KeyError(f"Blob ID {blob_id} not found")
        return self.blobs[blob_id]["data"]

    def info(self, blob_id: str) -> Dict[str, Any]:
        """Get metadata for a blob."""
        if blob_id not in self.metadata:
            raise KeyError(f"Blob ID {blob_id} not found")
        return self.metadata[blob_id]

    def delete(self, blob_id: str) -> None:
        """Delete a blob and its metadata."""
        self.blobs.pop(blob_id, None)
        self.metadata.pop(blob_id, None)
