
import os
import json
import time
from typing import Any
import uuid
from pathlib import Path


class LocalFileBlobStore:
    """File-based blob storage implementation."""

    def __init__(self, root: str | None = None, janitor_after_h: int = 24):
        """
        Initialize the local file blob store.
        Args:
            root: Root directory for blob storage (defaults to env BLOB_STORE_PATH or CWD/blobs).
            janitor_after_h: Number of hours after which blobs are eligible for cleanup
        """
        if root is None:
            root = os.environ.get(
                'BLOB_STORE_PATH', os.path.join(os.getcwd(), 'blobs'))
        self.root = Path(root)
        self.janitor_after_h = janitor_after_h
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, blob_id: str) -> str:
        """Get the file path for a blob's binary data."""
        return str(self.root / f"{blob_id}.bin")

    def _meta_path(self, blob_id: str) -> str:
        """Get the file path for a blob's metadata."""
        return str(self.root / f"{blob_id}.meta")

    def save(self, data: bytes, meta: dict[str, Any]) -> str:
        """
        Save binary data with metadata.
        Args:
            data: Binary data to store
            meta: Metadata dictionary
        Returns:
            Unique blob ID for the stored data
        """
        blob_id = str(uuid.uuid4())
        meta['created_at'] = time.time()

        with open(self._path(blob_id), 'wb') as f:
            f.write(data)

        with open(self._meta_path(blob_id), 'w') as f:
            json.dump(meta, f)

        return blob_id

    def load(self, blob_id: str) -> bytes:
        """
        Load binary data by blob ID.
        Args:
            blob_id: The blob ID to load
        Returns:
            Binary data
        Raises:
            FileNotFoundError: If the blob doesn't exist
        """
        path = self._path(blob_id)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Blob {blob_id} not found")

        with open(path, 'rb') as f:
            return f.read()

    def info(self, blob_id: str) -> dict[str, Any]:
        """
        Get metadata for a blob.
        Args:
            blob_id: The blob ID
        Returns:
            Metadata dictionary
        Raises:
            FileNotFoundError: If the blob doesn't exist
        """
        path = self._meta_path(blob_id)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Metadata for blob {blob_id} not found")

        with open(path, 'r') as f:
            return json.load(f)

    def delete(self, blob_id: str) -> None:
        """
        Delete a blob and its metadata.
        Args:
            blob_id: The blob ID to delete
        """
        bin_path = self._path(blob_id)
        meta_path = self._meta_path(blob_id)

        if os.path.exists(bin_path):
            os.unlink(bin_path)
        if os.path.exists(meta_path):
            os.unlink(meta_path)

    def purge_old(self) -> None:
        """Remove blobs older than the janitor threshold."""
        cutoff = time.time() - (self.janitor_after_h * 3600)

        for meta_file in self.root.glob('*.meta'):
            try:
                with open(meta_file, 'r') as f:
                    meta = json.load(f)
                if meta.get('created_at', float('inf')) < cutoff:
                    blob_id = meta_file.stem
                    self.delete(blob_id)
            except (json.JSONDecodeError, KeyError):
                continue
