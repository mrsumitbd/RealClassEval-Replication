
from typing import Any, Dict
import uuid
from collections import OrderedDict


class InMemoryBlobStore:

    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self.store: Dict[str, bytes] = {}
        self.metadata: Dict[str, Dict[str, Any]] = {}
        self.access_order = OrderedDict()

    def _evict_if_needed(self) -> None:
        while len(self.store) >= self.max_size:
            blob_id, _ = self.access_order.popitem(last=False)
            del self.store[blob_id]
            del self.metadata[blob_id]

    def save(self, data: bytes, meta: Dict[str, Any]) -> str:
        blob_id = str(uuid.uuid4())
        self._evict_if_needed()
        self.store[blob_id] = data
        self.metadata[blob_id] = meta
        self.access_order[blob_id] = None
        return blob_id

    def load(self, blob_id: str) -> bytes:
        if blob_id not in self.store:
            raise KeyError(f"Blob ID {blob_id} not found")
        self.access_order.move_to_end(blob_id)
        return self.store[blob_id]

    def info(self, blob_id: str) -> Dict[str, Any]:
        if blob_id not in self.metadata:
            raise KeyError(f"Blob ID {blob_id} not found")
        return self.metadata[blob_id]

    def delete(self, blob_id: str) -> None:
        if blob_id in self.store:
            del self.store[blob_id]
            del self.metadata[blob_id]
            del self.access_order[blob_id]
