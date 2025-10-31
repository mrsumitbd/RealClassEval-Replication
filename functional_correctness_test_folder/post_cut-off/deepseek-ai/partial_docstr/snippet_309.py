
import os
import json
import time
from typing import Any
from pathlib import Path
import uuid


class LocalFileBlobStore:

    def __init__(self, root: str | None = None, janitor_after_h: int = 24):
        '''
        Initialize the local file blob store.
        Args:
            root: Root directory for blob storage (defaults to env BLOB_STORE_PATH or CWD/blobs).
            janitor_after_h: Number of hours after which blobs are eligible for cleanup
        '''
        if root is None:
            root = os.getenv('BLOB_STORE_PATH',
                             os.path.join(os.getcwd(), 'blobs'))
        self.root = Path(root)
        self.janitor_after_h = janitor_after_h
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, blob_id: str) -> str:
        return str(self.root / f"{blob_id}.bin")

    def _meta_path(self, blob_id: str) -> str:
        return str(self.root / f"{blob_id}.meta")

    def save(self, data: bytes, meta: dict[str, Any]) -> str:
        blob_id = str(uuid.uuid4())
        data_path = self._path(blob_id)
        meta_path = self._meta_path(blob_id)

        with open(data_path, 'wb') as f:
            f.write(data)

        meta['timestamp'] = time.time()
        with open(meta_path, 'w') as f:
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
        data_path = self._path(blob_id)
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Blob {blob_id} not found")

        with open(data_path, 'rb') as f:
            return f.read()

    def info(self, blob_id: str) -> dict[str, Any]:
        meta_path = self._meta_path(blob_id)
        if not os.path.exists(meta_path):
            raise FileNotFoundError(f"Metadata for blob {blob_id} not found")

        with open(meta_path, 'r') as f:
            return json.load(f)

    def delete(self, blob_id: str) -> None:
        data_path = self._path(blob_id)
        meta_path = self._meta_path(blob_id)

        if os.path.exists(data_path):
            os.unlink(data_path)
        if os.path.exists(meta_path):
            os.unlink(meta_path)

    def purge_old(self) -> None:
        '''Remove blobs older than the janitor threshold.'''
        current_time = time.time()
        threshold = self.janitor_after_h * 3600

        for meta_file in self.root.glob("*.meta"):
            try:
                with open(meta_file, 'r') as f:
                    meta = json.load(f)
                timestamp = meta.get('timestamp', 0)
                if current_time - timestamp > threshold:
                    blob_id = meta_file.stem.split('.')[0]
                    self.delete(blob_id)
            except (json.JSONDecodeError, KeyError):
                continue
