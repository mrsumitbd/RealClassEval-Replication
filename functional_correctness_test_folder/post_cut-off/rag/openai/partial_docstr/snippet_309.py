
import os
import json
import uuid
import time
from pathlib import Path
from typing import Any, Dict, Optional


class LocalFileBlobStore:
    '''File‑based blob storage implementation.'''

    def __init__(self, root: Optional[str] = None, janitor_after_h: int = 24):
        '''
        Initialize the local file blob store.
        Args:
            root: Root directory for blob storage (defaults to env BLOB_STORE_PATH or CWD/blobs).
            janitor_after_h: Number of hours after which blobs are eligible for cleanup
        '''
        if root is None:
            root = os.getenv('BLOB_STORE_PATH')
            if not root:
                root = os.path.join(os.getcwd(), 'blobs')
        self.root = Path(root).expanduser().resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.janitor_after_h = janitor_after_h

    def _path(self, blob_id: str) -> Path:
        '''Get the file path for a blob's binary data.'''
        return self.root / blob_id

    def _meta_path(self, blob_id: str) -> Path:
        '''Get the file path for a blob's metadata.'''
        return self.root / f'{blob_id}.meta'

    def save(self, data: bytes, meta: Dict[str, Any]) -> str:
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

        # Write data
        with open(data_path, 'wb') as f:
            f.write(data)

        # Write metadata with timestamp
        meta_copy = dict(meta)
        meta_copy['created_at'] = time.time()
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(meta_copy, f)

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
        data_path = self._path(blob_id)
        if not data_path.is_file():
            raise FileNotFoundError(f'Blob data not found: {blob_id}')
        with open(data_path, 'rb') as f:
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
        meta_path = self._meta_path(blob_id)
        if not meta_path.is_file():
            raise FileNotFoundError(f'Blob metadata not found: {blob_id}')
        with open(meta_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def delete(self, blob_id: str) -> None:
        '''
        Delete a blob and its metadata.
        Args:
            blob_id: The blob ID to delete
        '''
        data_path = self._path(blob_id)
        meta_path = self._meta_path(blob_id)
        for p in (data_path, meta_path):
            try:
                p.unlink()
            except FileNotFoundError:
                pass

    def purge_old(self) -> None:
        '''Remove blobs older than the janitor threshold.'''
        threshold_ts = time.time() - self.janitor_after_h * 3600
        for meta_file in self.root.glob('*.meta'):
            try:
                with open(meta_file, 'r', encoding='utf-8') as f:
                    meta = json.load(f)
                created_at = meta.get('created_at')
                if created_at is None:
                    continue
                if created_at < threshold_ts:
                    blob_id = meta_file.stem
                    self.delete(blob_id)
            except Exception:
                # Skip files that cannot be read or parsed
                continue
