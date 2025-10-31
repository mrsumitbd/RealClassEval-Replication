
import os
import hashlib
import json
import time
from typing import Any, Dict


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
        self.root = root
        self.janitor_after_h = janitor_after_h
        os.makedirs(self.root, exist_ok=True)

    def _path(self, blob_id: str) -> str:
        """Get the file path for a blob's binary data."""
        return os.path.join(self.root, blob_id[:2], blob_id[2:])

    def _meta_path(self, blob_id: str) -> str:
        """Get the file path for a blob's metadata."""
        return self._path(blob_id) + '.meta'

    def save(self, data: bytes, meta: Dict[str, Any]) -> str:
        """
        Save binary data with metadata.

        Args:
            data: Binary data to store
            meta: Metadata dictionary

        Returns:
            Unique blob ID for the stored data
        """
        blob_id = hashlib.sha256(data).hexdigest()
        path = self._path(blob_id)
        meta_path = self._meta_path(blob_id)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(data)
        meta['created_at'] = time.time()
        with open(meta_path, 'w') as f:
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
        try:
            with open(path, 'rb') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f'Blob {blob_id} not found')

    def info(self, blob_id: str) -> Dict[str, Any]:
        """
        Get metadata for a blob.

        Args:
            blob_id: The blob ID

        Returns:
            Metadata dictionary

        Raises:
            FileNotFoundError: If the blob doesn't exist
        """
        meta_path = self._meta_path(blob_id)
        try:
            with open(meta_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f'Blob {blob_id} not found')

    def delete(self, blob_id: str) -> None:
        """
        Delete a blob and its metadata.

        Args:
            blob_id: The blob ID to delete
        """
        path = self._path(blob_id)
        meta_path = self._meta_path(blob_id)
        try:
            os.unlink(path)
        except FileNotFoundError:
            pass
        try:
            os.unlink(meta_path)
        except FileNotFoundError:
            pass

    def purge_old(self) -> None:
        """Remove blobs older than the janitor threshold."""
        cutoff = time.time() - self.janitor_after_h * 3600
        for root, dirs, files in os.walk(self.root):
            for file in files:
                if file.endswith('.meta'):
                    meta_path = os.path.join(root, file)
                    with open(meta_path, 'r') as f:
                        meta = json.load(f)
                    if meta['created_at'] < cutoff:
                        blob_id = file[:-5]
                        self.delete(blob_id)
