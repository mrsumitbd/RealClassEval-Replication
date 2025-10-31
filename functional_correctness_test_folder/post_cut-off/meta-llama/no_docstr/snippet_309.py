
import os
import uuid
import json
import time
from typing import Any


class LocalFileBlobStore:

    def __init__(self, root: str | None = None, janitor_after_h: int = 24):
        if root is None:
            root = './blob_store'
        self.root = root
        self.janitor_after_h = janitor_after_h
        os.makedirs(self.root, exist_ok=True)

    def _path(self, blob_id: str) -> str:
        return os.path.join(self.root, blob_id)

    def _meta_path(self, blob_id: str) -> str:
        return os.path.join(self.root, f'{blob_id}.meta')

    def save(self, data: bytes, meta: dict[str, Any]) -> str:
        blob_id = str(uuid.uuid4())
        with open(self._path(blob_id), 'wb') as f:
            f.write(data)
        meta['created_at'] = time.time()
        with open(self._meta_path(blob_id), 'w') as f:
            json.dump(meta, f)
        return blob_id

    def load(self, blob_id: str) -> bytes:
        with open(self._path(blob_id), 'rb') as f:
            return f.read()

    def info(self, blob_id: str) -> dict[str, Any]:
        with open(self._meta_path(blob_id), 'r') as f:
            return json.load(f)

    def delete(self, blob_id: str) -> None:
        try:
            os.remove(self._path(blob_id))
            os.remove(self._meta_path(blob_id))
        except FileNotFoundError:
            pass

    def purge_old(self) -> None:
        cutoff = time.time() - self.janitor_after_h * 3600
        for filename in os.listdir(self.root):
            if filename.endswith('.meta'):
                blob_id = filename[:-5]
                meta_path = self._meta_path(blob_id)
                try:
                    with open(meta_path, 'r') as f:
                        meta = json.load(f)
                    if meta['created_at'] < cutoff:
                        self.delete(blob_id)
                except FileNotFoundError:
                    pass
                except json.JSONDecodeError:
                    pass
