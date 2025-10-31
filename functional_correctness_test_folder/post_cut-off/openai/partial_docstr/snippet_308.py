
import uuid
from collections import OrderedDict
from typing import Any, Dict


class InMemoryBlobStore:
    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self._store: "OrderedDict[str, tuple[bytes, dict[str, Any]]]" = OrderedDict(
        )

    def _evict_if_needed(self) -> None:
        """Evict oldest blobs if we've exceeded max_size."""
        while len(self._store) > self.max_size:
            self._store.popitem(last=False)

    def save(self, data: bytes, meta: dict[str, Any]) -> str:
        """Save binary data with metadata."""
        blob_id = uuid.uuid4().hex
        self._store[blob_id] = (data, meta)
        self._evict_if_needed()
        return blob_id

    def load(self, blob_id: str) -> bytes:
        if blob_id not in self._store:
            raise KeyError(f"Blob ID {blob_id} not found")
        return self._store[blob_id][0]

    def info(self, blob_id: str) -> dict[str, Any]:
        """Get metadata for a blob."""
        if blob_id not in self._store:
            raise KeyError(f"Blob ID {blob_id} not found")
        return self._store[blob_id][1]

    def delete(self, blob_id: str) -> None:
        if blob_id not in self._store:
            raise KeyError(f"Blob ID {blob_id} not found")
        del self._store[blob_id]
