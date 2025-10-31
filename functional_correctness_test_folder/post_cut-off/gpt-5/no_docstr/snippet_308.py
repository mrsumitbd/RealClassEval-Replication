from __future__ import annotations

from collections import OrderedDict
from typing import Any
from uuid import uuid4
from datetime import datetime


class InMemoryBlobStore:
    def __init__(self, max_size: int = 100):
        if not isinstance(max_size, int) or max_size <= 0:
            raise ValueError("max_size must be a positive integer")
        self.max_size = max_size
        self._store: "OrderedDict[str, dict[str, Any]]" = OrderedDict()

    def _evict_if_needed(self) -> None:
        while len(self._store) > self.max_size:
            self._store.popitem(last=False)

    def save(self, data: bytes, meta: dict[str, Any]) -> str:
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise TypeError("data must be bytes-like")
        blob_id = uuid4().hex
        while blob_id in self._store:
            blob_id = uuid4().hex
        meta_copy = dict(meta or {})
        meta_copy.setdefault("size", len(data))
        meta_copy.setdefault("created_at", datetime.utcnow().isoformat() + "Z")
        self._store[blob_id] = {
            "data": bytes(data),
            "meta": meta_copy,
        }
        self._store.move_to_end(blob_id, last=True)
        self._evict_if_needed()
        return blob_id

    def load(self, blob_id: str) -> bytes:
        try:
            entry = self._store[blob_id]
        except KeyError:
            raise KeyError(f"blob_id not found: {blob_id}")
        self._store.move_to_end(blob_id, last=True)
        return entry["data"]

    def info(self, blob_id: str) -> dict[str, Any]:
        try:
            entry = self._store[blob_id]
        except KeyError:
            raise KeyError(f"blob_id not found: {blob_id}")
        self._store.move_to_end(blob_id, last=True)
        info = dict(entry["meta"])
        info.setdefault("id", blob_id)
        return info

    def delete(self, blob_id: str) -> None:
        try:
            del self._store[blob_id]
        except KeyError:
            raise KeyError(f"blob_id not found: {blob_id}")
