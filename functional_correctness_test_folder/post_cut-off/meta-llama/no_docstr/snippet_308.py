
from typing import Any
from collections import OrderedDict
import uuid


class InMemoryBlobStore:

    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self.blob_store = OrderedDict()

    def _evict_if_needed(self) -> None:
        if len(self.blob_store) >= self.max_size:
            blob_id, _ = self.blob_store.popitem(last=False)
            del _

    def save(self, data: bytes, meta: dict[str, Any]) -> str:
        blob_id = str(uuid.uuid4())
        self.blob_store[blob_id] = (data, meta)
        self._evict_if_needed()
        return blob_id

    def load(self, blob_id: str) -> bytes:
        if blob_id not in self.blob_store:
            raise KeyError(f"Blob {blob_id} not found")
        data, _ = self.blob_store[blob_id]
        self.blob_store.move_to_end(blob_id)
        return data

    def info(self, blob_id: str) -> dict[str, Any]:
        if blob_id not in self.blob_store:
            raise KeyError(f"Blob {blob_id} not found")
        _, meta = self.blob_store[blob_id]
        self.blob_store.move_to_end(blob_id)
        return meta

    def delete(self, blob_id: str) -> None:
        if blob_id in self.blob_store:
            del self.blob_store[blob_id]
