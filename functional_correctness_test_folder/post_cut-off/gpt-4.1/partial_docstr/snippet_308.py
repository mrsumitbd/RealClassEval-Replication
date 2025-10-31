
import uuid
from collections import OrderedDict
from typing import Any


class InMemoryBlobStore:

    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self._blobs = OrderedDict()  # blob_id -> (data, meta)

    def _evict_if_needed(self) -> None:
        while len(self._blobs) > self.max_size:
            self._blobs.popitem(last=False)

    def save(self, data: bytes, meta: dict[str, Any]) -> str:
        blob_id = str(uuid.uuid4())
        self._blobs[blob_id] = (data, dict(meta))
        self._evict_if_needed()
        return blob_id

    def load(self, blob_id: str) -> bytes:
        if blob_id not in self._blobs:
            raise KeyError(f"Blob ID {blob_id} not found")
        return self._blobs[blob_id][0]

    def info(self, blob_id: str) -> dict[str, Any]:
        if blob_id not in self._blobs:
            raise KeyError(f"Blob ID {blob_id} not found")
        return dict(self._blobs[blob_id][1])

    def delete(self, blob_id: str) -> None:
        if blob_id not in self._blobs:
            raise KeyError(f"Blob ID {blob_id} not found")
        del self._blobs[blob_id]
