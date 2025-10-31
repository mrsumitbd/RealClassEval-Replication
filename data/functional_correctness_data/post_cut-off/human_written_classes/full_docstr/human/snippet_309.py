import json
from typing import Any, Protocol
import uuid
import os
import time

class LocalFileBlobStore:
    """File-based blob storage implementation."""

    def __init__(self, root: str | None=None, janitor_after_h: int=24):
        """
        Initialize the local file blob store.

        Args:
            root: Root directory for blob storage (defaults to env BLOB_STORE_PATH or CWD/blobs).            janitor_after_h: Number of hours after which blobs are eligible for cleanup
        """
        self.root = root or os.getenv('BLOB_STORE_PATH', os.path.join(os.getcwd(), 'blobs'))
        self.janitor_after = janitor_after_h * 3600
        os.makedirs(self.root, exist_ok=True)
        logger.debug(f'Initialized blob store at {self.root}')

    def _path(self, blob_id: str) -> str:
        """Get the file path for a blob's binary data."""
        return os.path.join(self.root, f'{blob_id}.bin')

    def _meta_path(self, blob_id: str) -> str:
        """Get the file path for a blob's metadata."""
        return os.path.join(self.root, f'{blob_id}.json')

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
        with open(self._path(blob_id), 'wb') as f:
            f.write(data)
        meta_with_ts = meta.copy()
        meta_with_ts['ts'] = time.time()
        meta_with_ts['size'] = len(data)
        with open(self._meta_path(blob_id), 'w') as f:
            json.dump(meta_with_ts, f)
        logger.debug(f'Stored blob {blob_id} ({len(data)} bytes)')
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
        blob_path = self._path(blob_id)
        if not os.path.exists(blob_path):
            raise FileNotFoundError(f'Blob {blob_id} not found')
        with open(blob_path, 'rb') as f:
            data = f.read()
        logger.debug(f'Loaded blob {blob_id} ({len(data)} bytes)')
        return data

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
        meta_path = self._meta_path(blob_id)
        if not os.path.exists(meta_path):
            raise FileNotFoundError(f'Blob {blob_id} metadata not found')
        with open(meta_path) as f:
            return json.load(f)

    def delete(self, blob_id: str) -> None:
        """
        Delete a blob and its metadata.

        Args:
            blob_id: The blob ID to delete
        """
        for path in (self._path(blob_id), self._meta_path(blob_id)):
            if os.path.exists(path):
                os.remove(path)
                logger.debug(f'Deleted {path}')

    def purge_old(self) -> None:
        """Remove blobs older than the janitor threshold."""
        threshold = time.time() - self.janitor_after
        purged_count = 0
        try:
            for fname in os.listdir(self.root):
                if fname.endswith('.json'):
                    meta_path = os.path.join(self.root, fname)
                    try:
                        with open(meta_path) as f:
                            meta = json.load(f)
                        if meta.get('ts', 0) < threshold:
                            blob_id = fname[:-5]
                            self.delete(blob_id)
                            purged_count += 1
                    except (json.JSONDecodeError, OSError) as e:
                        logger.warning(f'Error processing {meta_path}: {e}')
            if purged_count > 0:
                logger.info(f'Purged {purged_count} old blobs')
        except OSError as e:
            logger.warning(f'Error during purge: {e}')