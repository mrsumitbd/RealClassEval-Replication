import os
import json
import hashlib
import time
from typing import Any


class LocalFileBlobStore:
    '''File-based blob storage implementation.'''

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
        '''Get the file path for a blob's binary data.'''
        return os.path.join(self.root, f"{blob_id}.bin")

    def _meta_path(self, blob_id: str) -> str:
        '''Get the file path for a blob's metadata.'''
        return os.path.join(self.root, f"{blob_id}.json")

    def save(self, data: bytes, meta: dict[str, Any]) -> str:
        '''
        Save binary data with metadata.
        Args:
            data: Binary data to store
            meta: Metadata dictionary
        Returns:
            Unique blob ID for the stored data
        '''
        h = hashlib.sha256(data).hexdigest()
        bin_path = self._path(h)
        meta_path = self._meta_path(h)
        # Save binary data
        with open(bin_path, "wb") as f:
            f.write(data)
        # Save metadata (add timestamp)
        meta = dict(meta)  # copy
        meta["saved_at"] = int(time.time())
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f)
        return h

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
        bin_path = self._path(blob_id)
        if not os.path.isfile(bin_path):
            raise FileNotFoundError(f"Blob data not found: {blob_id}")
        with open(bin_path, "rb") as f:
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
        if not os.path.isfile(meta_path):
            raise FileNotFoundError(f"Blob metadata not found: {blob_id}")
        with open(meta_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def delete(self, blob_id: str) -> None:
        '''
        Delete a blob and its metadata.
        Args:
            blob_id: The blob ID to delete
        '''
        bin_path = self._path(blob_id)
        meta_path = self._meta_path(blob_id)
        for p in (bin_path, meta_path):
            try:
                os.remove(p)
            except FileNotFoundError:
                pass

    def purge_old(self) -> None:
        '''Remove blobs older than the janitor threshold.'''
        now = int(time.time())
        threshold = now - self.janitor_after_h * 3600
        for fname in os.listdir(self.root):
            if fname.endswith(".json"):
                meta_path = os.path.join(self.root, fname)
                try:
                    with open(meta_path, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                    saved_at = meta.get("saved_at")
                    if saved_at is not None and saved_at < threshold:
                        blob_id = fname[:-5]
                        self.delete(blob_id)
                except Exception:
                    continue
