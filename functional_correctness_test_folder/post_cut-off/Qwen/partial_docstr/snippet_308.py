
from typing import Any, Dict
import uuid
from collections import OrderedDict


class InMemoryBlobStore:

    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self.blobs: OrderedDict[str, bytes] = OrderedDict()
        self.metadata: Dict[str, Dict[str, Any]] = OrderedDict()

    def _evict_if_needed(self) -> None:
        while len(self.blobs) > self.max_size:
            oldest_blob_id = next(iter(self.blobs))
            del self.blobs[oldest_blob_id]
            del self.metadata[oldest_blob_id]

    def save(self, data: bytes, meta: Dict[str, Any]) -> str:
        blob_id = str(uuid.uuid4())
        self.blobs[blob_id] = data
        self.metadata[blob_id] = meta
        self._evict_if_needed()
        return blob_id

    def load(self, blob_id: str) -> bytes:
        if blob_id in self.blobs:
            self.blobs.move_to_end(blob_id)
            return self.blobs[blob_id]
        raise KeyError(f"No blob found with id: {blob_id}")

    def info(self, blob_id: str) -> Dict[str, Any]:
        if blob_id in self.metadata:
            self.metadata.move_to_end(blob_id)
            return self.metadata[blob_id]
        raise KeyError(f"No metadata found for blob id: {blob_id}")

    def delete(self, blob_id: str) -> None:
        if blob_id in self.blobs:
            del self.blobs[blob_id]
            del self.metadata[blob_id]
        else:
            raise KeyError(f"No blob found with id: {blob_id}")
