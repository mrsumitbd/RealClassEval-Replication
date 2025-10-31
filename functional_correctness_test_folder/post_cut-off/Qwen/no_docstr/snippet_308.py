
from typing import Any, Dict
import uuid


class InMemoryBlobStore:

    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self.store: Dict[str, Dict[str, Any]] = {}
        self.order: list[str] = []

    def _evict_if_needed(self) -> None:
        while len(self.store) >= self.max_size:
            oldest_blob_id = self.order.pop(0)
            del self.store[oldest_blob_id]

    def save(self, data: bytes, meta: Dict[str, Any]) -> str:
        blob_id = str(uuid.uuid4())
        self._evict_if_needed()
        self.store[blob_id] = {'data': data, 'meta': meta}
        self.order.append(blob_id)
        return blob_id

    def load(self, blob_id: str) -> bytes:
        return self.store[blob_id]['data']

    def info(self, blob_id: str) -> Dict[str, Any]:
        return self.store[blob_id]['meta']

    def delete(self, blob_id: str) -> None:
        if blob_id in self.store:
            self.order.remove(blob_id)
            del self.store[blob_id]
