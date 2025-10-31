from typing import Any, Protocol
import time
import uuid

class InMemoryBlobStore:
    """In-memory blob storage for testing and short-lived scenarios."""

    def __init__(self, max_size: int=100):
        """
        Initialize in-memory blob store.

        Args:
            max_size: Maximum number of blobs to keep in memory
        """
        self.blobs: dict[str, bytes] = {}
        self.metadata: dict[str, dict[str, Any]] = {}
        self.max_size = max_size
        self.access_order: list[str] = []

    def _evict_if_needed(self) -> None:
        """Evict oldest blobs if we've exceeded max_size."""
        while len(self.blobs) >= self.max_size and self.access_order:
            oldest_id = self.access_order.pop(0)
            self.blobs.pop(oldest_id, None)
            self.metadata.pop(oldest_id, None)

    def save(self, data: bytes, meta: dict[str, Any]) -> str:
        """Save binary data with metadata."""
        self._evict_if_needed()
        blob_id = str(uuid.uuid4())
        self.blobs[blob_id] = data
        meta_with_ts = meta.copy()
        meta_with_ts['ts'] = time.time()
        meta_with_ts['size'] = len(data)
        self.metadata[blob_id] = meta_with_ts
        self.access_order.append(blob_id)
        return blob_id

    def load(self, blob_id: str) -> bytes:
        """Load binary data by blob ID."""
        if blob_id not in self.blobs:
            raise FileNotFoundError(f'Blob {blob_id} not found')
        if blob_id in self.access_order:
            self.access_order.remove(blob_id)
        self.access_order.append(blob_id)
        return self.blobs[blob_id]

    def info(self, blob_id: str) -> dict[str, Any]:
        """Get metadata for a blob."""
        if blob_id not in self.metadata:
            raise FileNotFoundError(f'Blob {blob_id} metadata not found')
        return self.metadata[blob_id].copy()

    def delete(self, blob_id: str) -> None:
        """Delete a blob and its metadata."""
        self.blobs.pop(blob_id, None)
        self.metadata.pop(blob_id, None)
        if blob_id in self.access_order:
            self.access_order.remove(blob_id)