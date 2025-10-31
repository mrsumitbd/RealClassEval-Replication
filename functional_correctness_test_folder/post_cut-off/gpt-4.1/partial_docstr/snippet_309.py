
import os
import json
import uuid
import shutil
import time
from typing import Any
from datetime import datetime, timedelta


class LocalFileBlobStore:

    def __init__(self, root: str | None = None, janitor_after_h: int = 24):
        '''
        Initialize the local file blob store.
        Args:
            root: Root directory for blob storage (defaults to env BLOB_STORE_PATH or CWD/blobs).
            janitor_after_h: Number of hours after which blobs are eligible for cleanup
        '''
        if root is None:
            root = os.environ.get("BLOB_STORE_PATH")
            if root is None:
                root = os.path.join(os.getcwd(), "blobs")
        self.root = os.path.abspath(root)
        self.janitor_after_h = janitor_after_h
        os.makedirs(self.root, exist_ok=True)

    def _path(self, blob_id: str) -> str:
        return os.path.join(self.root, f"{blob_id}.blob")

    def _meta_path(self, blob_id: str) -> str:
        return os.path.join(self.root, f"{blob_id}.meta.json")

    def save(self, data: bytes, meta: dict[str, Any]) -> str:
        blob_id = uuid.uuid4().hex
        blob_path = self._path(blob_id)
        meta_path = self._meta_path(blob_id)
        with open(blob_path, "wb") as f:
            f.write(data)
        meta = dict(meta)  # copy
        meta["created"] = time.time()
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f)
        return blob_id

    def load(self, blob_id: str) -> bytes:
        '''
        Load binary data by blob ID.
        Args:
            blob_id: The blob ID to load
        Returns:
            Binary data
        Raises:
            FileNotFoundError: If the blob doesn't exist
        '''
        blob_path = self._path(blob_id)
        if not os.path.exists(blob_path):
            raise FileNotFoundError(f"Blob {blob_id} not found")
        with open(blob_path, "rb") as f:
            return f.read()

    def info(self, blob_id: str) -> dict[str, Any]:
        meta_path = self._meta_path(blob_id)
        if not os.path.exists(meta_path):
            raise FileNotFoundError(f"Metadata for blob {blob_id} not found")
        with open(meta_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def delete(self, blob_id: str) -> None:
        blob_path = self._path(blob_id)
        meta_path = self._meta_path(blob_id)
        if os.path.exists(blob_path):
            os.remove(blob_path)
        if os.path.exists(meta_path):
            os.remove(meta_path)

    def purge_old(self) -> None:
        '''Remove blobs older than the janitor threshold.'''
        now = time.time()
        threshold = now - self.janitor_after_h * 3600
        for fname in os.listdir(self.root):
            if fname.endswith(".meta.json"):
                meta_path = os.path.join(self.root, fname)
                try:
                    with open(meta_path, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                    created = meta.get("created")
                    if created is not None and created < threshold:
                        blob_id = fname[:-10]  # remove .meta.json
                        self.delete(blob_id)
                except Exception:
                    continue
