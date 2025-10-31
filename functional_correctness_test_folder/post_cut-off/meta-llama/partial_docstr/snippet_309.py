
import os
import uuid
import json
from datetime import datetime, timedelta
from typing import Any


class LocalFileBlobStore:

    def __init__(self, root: str | None = None, janitor_after_h: int = 24):
        '''
        Initialize the local file blob store.
        Args:
            root: Root directory for blob storage (defaults to env BLOB_STORE_PATH or CWD/blobs).
            janitor_after_h: Number of hours after which blobs are eligible for cleanup
        '''
        self.root = root or os.environ.get(
            'BLOB_STORE_PATH', os.path.join(os.getcwd(), 'blobs'))
        os.makedirs(self.root, exist_ok=True)
        self.janitor_after_h = janitor_after_h

    def _path(self, blob_id: str) -> str:
        return os.path.join(self.root, blob_id)

    def _meta_path(self, blob_id: str) -> str:
        return os.path.join(self.root, f'{blob_id}.meta')

    def save(self, data: bytes, meta: dict[str, Any]) -> str:
        blob_id = str(uuid.uuid4())
        with open(self._path(blob_id), 'wb') as f:
            f.write(data)
        with open(self._meta_path(blob_id), 'w') as f:
            meta['created_at'] = datetime.now().isoformat()
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
        try:
            with open(self._path(blob_id), 'rb') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f'Blob {blob_id} not found')

    def info(self, blob_id: str) -> dict[str, Any]:
        try:
            with open(self._meta_path(blob_id), 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f'Blob {blob_id} not found')

    def delete(self, blob_id: str) -> None:
        try:
            os.remove(self._path(blob_id))
            os.remove(self._meta_path(blob_id))
        except FileNotFoundError:
            pass

    def purge_old(self) -> None:
        '''Remove blobs older than the janitor threshold.'''
        threshold = datetime.now() - timedelta(hours=self.janitor_after_h)
        for filename in os.listdir(self.root):
            if filename.endswith('.meta'):
                blob_id = filename[:-5]
                meta_path = self._meta_path(blob_id)
                try:
                    with open(meta_path, 'r') as f:
                        meta = json.load(f)
                        created_at = datetime.fromisoformat(meta['created_at'])
                        if created_at < threshold:
                            self.delete(blob_id)
                except (FileNotFoundError, json.JSONDecodeError):
                    pass
