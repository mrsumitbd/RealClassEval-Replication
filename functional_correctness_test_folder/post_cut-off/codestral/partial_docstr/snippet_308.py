
import uuid
from typing import Any, Dict, List, Tuple


class InMemoryBlobStore:

    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self.blobs: Dict[str, Tuple[bytes, Dict[str, Any]]] = {}
        self.access_order: List[str] = []

    def _evict_if_needed(self) -> None:
        while len(self.blobs) > self.max_size:
            oldest_blob_id = self.access_order.pop(0)
            del self.blobs[oldest_blob_id]

    def save(self, data: bytes, meta: dict[str, Any]) -> str:
        blob_id = str(uuid.uuid4())
        self.blobs[blob_id] = (data, meta)
        self.access_order.append(blob_id)
        self._evict_if_needed()
        return blob_id

    def load(self, blob_id: str) -> bytes:
        if blob_id in self.blobs:
            self.access_order.remove(blob_id)
            self.access_order.append(blob_id)
            return self.blobs[blob_id][0]
        raise KeyError(f"Blob ID {blob_id} not found")

    def info(self, blob_id: str) -> dict[str, Any]:
        if blob_id in self.blobs:
            self.access_order.remove(blob_id)
            self.access_order.append(blob_id)
            return self.blobs[blob_id][1]
        raise KeyError(f"Blob ID {blob_id} not found")

    def delete(self, blob_id: str) -> None:
        if blob_id in self.blobs:
            del self.blobs[blob_id]
            self.access_order.remove(blob_id)
        else:
            raise KeyError(f"Blob ID {blob_id} not found")
