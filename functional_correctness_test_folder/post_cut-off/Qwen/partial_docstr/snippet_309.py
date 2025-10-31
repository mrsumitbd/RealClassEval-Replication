
import os
import json
import time
from typing import Any, Dict
from pathlib import Path
from datetime import datetime, timedelta


class LocalFileBlobStore:

    def __init__(self, root: str | None = None, janitor_after_h: int = 24):
        self.root = Path(root) if root else Path(
            os.getenv('BLOB_STORE_PATH', 'blobs'))
        self.janitor_after_h = janitor_after_h
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, blob_id: str) -> str:
        return str(self.root / f"{blob_id}.bin")

    def _meta_path(self, blob_id: str) -> str:
        return str(self.root / f"{blob_id}.meta")

    def save(self, data: bytes, meta: Dict[str, Any]) -> str:
        blob_id = str(time.time_ns())
        with open(self._path(blob_id), 'wb') as f:
            f.write(data)
        meta['created_at'] = datetime.now().isoformat()
        with open(self._meta_path(blob_id), 'w') as f:
            json.dump(meta, f)
        return blob_id

    def load(self, blob_id: str) -> bytes:
        path = self._path(blob_id)
        if not os.path.exists(path):
            raise FileNotFoundError(f"No blob found with ID: {blob_id}")
        with open(path, 'rb') as f:
            return f.read()

    def info(self, blob_id: str) -> Dict[str, Any]:
        meta_path = self._meta_path(blob_id)
        if not os.path.exists(meta_path):
            raise FileNotFoundError(
                f"No metadata found for blob ID: {blob_id}")
        with open(meta_path, 'r') as f:
            return json.load(f)

    def delete(self, blob_id: str) -> None:
        os.remove(self._path(blob_id))
        os.remove(self._meta_path(blob_id))

    def purge_old(self) -> None:
        cutoff_time = datetime.now() - timedelta(hours=self.janitor_after_h)
        for blob_id in os.listdir(self.root):
            if blob_id.endswith('.meta'):
                blob_id = blob_id[:-5]
                meta = self.info(blob_id)
                created_at = datetime.fromisoformat(meta['created_at'])
                if created_at < cutoff_time:
                    self.delete(blob_id)
