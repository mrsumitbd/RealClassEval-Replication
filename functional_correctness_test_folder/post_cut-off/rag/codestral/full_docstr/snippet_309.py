
import os
import json
import time
from typing import Any, Dict, Optional


class LocalFileBlobStore:
    '''File-based blob storage implementation.'''

    def __init__(self, root: Optional[str] = None, janitor_after_h: int = 24):
        '''
        Initialize the local file blob store.
        Args:
            root: Root directory for blob storage (defaults to env BLOB_STORE_PATH or CWD/blobs).
            janitor_after_h: Number of hours after which blobs are eligible for cleanup
        '''
        self.root = root or os.getenv(
            'BLOB_STORE_PATH', os.path.join(os.getcwd(), 'blobs'))
        self.janitor_after_h = janitor_after_h
        os.makedirs(self.root, exist_ok=True)

    def _path(self, blob_id: str) -> str:
        '''Get the file path for a blob's binary data.'''
        return os.path.join(self.root, f'{blob_id}.bin')

    def _meta_path(self, blob_id: str) -> str:
        '''Get the file path for a blob's metadata.'''
        return os.path.join(self.root, f'{blob_id}.meta')

    def save(self, data: bytes, meta: Dict[str, Any]) -> str:
        '''
        Save binary data with metadata.
        Args:
            data: Binary data to store
            meta: Metadata dictionary
        Returns:
            Unique blob ID for the stored data
        '''
        blob_id = os.urandom(16).hex()
        with open(self._path(blob_id), 'wb') as f:
            f.write(data)
        with open(self._meta_path(blob_id), 'w') as f:
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
        with open(self._path(blob_id), 'rb') as f:
            return f.read()

    def info(self, blob_id: str) -> Dict[str, Any]:
        '''
        Get metadata for a blob.
        Args:
            blob_id: The blob ID
        Returns:
            Metadata dictionary
        Raises:
            FileNotFoundError: If the blob doesn't exist
        '''
        with open(self._meta_path(blob_id), 'r') as f:
            return json.load(f)

    def delete(self, blob_id: str) -> None:
        '''
        Delete a blob and its metadata.
        Args:
            blob_id: The blob ID to delete
        '''
        os.remove(self._path(blob_id))
        os.remove(self._meta_path(blob_id))

    def purge_old(self) -> None:
        '''Remove blobs older than the janitor threshold.'''
        now = time.time()
        threshold = now - (self.janitor_after_h * 3600)

        for filename in os.listdir(self.root):
            if filename.endswith('.meta'):
                blob_id = filename[:-5]
                meta_path = self._meta_path(blob_id)
                try:
                    with open(meta_path, 'r') as f:
                        meta = json.load(f)
                    if 'timestamp' in meta and meta['timestamp'] < threshold:
                        self.delete(blob_id)
                except (FileNotFoundError, json.JSONDecodeError):
                    continue
