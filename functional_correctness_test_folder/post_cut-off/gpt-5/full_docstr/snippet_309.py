import os
import json
import time
import uuid
import tempfile
from typing import Any


class LocalFileBlobStore:
    '''File-based blob storage implementation.'''

    def __init__(self, root: str | None = None, janitor_after_h: int = 24):
        '''
        Initialize the local file blob store.
        Args:
            root: Root directory for blob storage (defaults to env BLOB_STORE_PATH or CWD/blobs).            janitor_after_h: Number of hours after which blobs are eligible for cleanup
        '''
        root_dir = root or os.environ.get(
            "BLOB_STORE_PATH") or os.path.join(os.getcwd(), "blobs")
        self.root = os.path.abspath(root_dir)
        self.data_dir = os.path.join(self.root, "data")
        self.meta_dir = os.path.join(self.root, "meta")
        self.janitor_after_h = int(janitor_after_h)
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.meta_dir, exist_ok=True)

    def _path(self, blob_id: str) -> str:
        '''Get the file path for a blob's binary data.'''
        return os.path.join(self.data_dir, f"{blob_id}.bin")

    def _meta_path(self, blob_id: str) -> str:
        '''Get the file path for a blob's metadata.'''
        return os.path.join(self.meta_dir, f"{blob_id}.json")

    def save(self, data: bytes, meta: dict[str, Any]) -> str:
        '''
        Save binary data with metadata.
        Args:
            data: Binary data to store
            meta: Metadata dictionary
        Returns:
            Unique blob ID for the stored data
        '''
        blob_id = uuid.uuid4().hex
        data_path = self._path(blob_id)
        meta_path = self._meta_path(blob_id)

        # Write data atomically
        with tempfile.NamedTemporaryFile(delete=False, dir=self.data_dir) as tf:
            tf.write(data)
            temp_data_path = tf.name
        os.replace(temp_data_path, data_path)

        # Prepare metadata
        now_ts = time.time()
        meta_to_store = dict(meta or {})
        meta_to_store.setdefault("created_at_ts", now_ts)
        meta_to_store.setdefault("size", len(data))
        meta_to_store.setdefault("blob_id", blob_id)

        # Write meta atomically
        meta_json = json.dumps(
            meta_to_store, ensure_ascii=False, separators=(",", ":"))
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=self.meta_dir) as tfm:
            tfm.write(meta_json)
            temp_meta_path = tfm.name
        os.replace(temp_meta_path, meta_path)

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
        path = self._path(blob_id)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Blob data not found: {blob_id}")
        with open(path, "rb") as f:
            return f.read()

    def info(self, blob_id: str) -> dict[str, Any]:
        '''
        Get metadata for a blob.
        Args:
            blob_id: The blob ID
        Returns:
            Metadata dictionary
        Raises:
            FileNotFoundError: If the blob doesn't exist
        '''
        meta_path = self._meta_path(blob_id)
        if not os.path.exists(meta_path):
            raise FileNotFoundError(f"Blob metadata not found: {blob_id}")
        with open(meta_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def delete(self, blob_id: str) -> None:
        '''
        Delete a blob and its metadata.
        Args:
            blob_id: The blob ID to delete
        '''
        for p in (self._path(blob_id), self._meta_path(blob_id)):
            try:
                os.remove(p)
            except FileNotFoundError:
                pass

    def purge_old(self) -> None:
        '''Remove blobs older than the janitor threshold.'''
        threshold_s = self.janitor_after_h * 3600
        now = time.time()

        try:
            entries = [f for f in os.listdir(
                self.meta_dir) if f.endswith(".json")]
        except FileNotFoundError:
            return

        for fname in entries:
            blob_id = fname[:-5]
            meta_path = os.path.join(self.meta_dir, fname)
            created_ts = None
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                created_ts = meta.get("created_at_ts")
            except Exception:
                pass

            if created_ts is None:
                try:
                    created_ts = os.path.getmtime(meta_path)
                except OSError:
                    created_ts = None

            if created_ts is None:
                continue

            if (now - float(created_ts)) >= threshold_s:
                self.delete(blob_id)
