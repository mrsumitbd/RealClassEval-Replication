
import os
import json
import uuid
import time
from typing import Any, Dict, Union


class LocalFileBlobStore:

    def __init__(self, root: Union[str, None] = None, janitor_after_h: int = 24):
        self.root = root if root is not None else os.path.join(
            os.getcwd(), 'blob_store')
        self.janitor_after_h = janitor_after_h
        os.makedirs(self.root, exist_ok=True)

    def _path(self, blob_id: str) -> str:
        return os.path.join(self.root, blob_id)

    def _meta_path(self, blob_id: str) -> str:
        return os.path.join(self.root, f"{blob_id}.meta")

    def save(self, data: bytes, meta: Dict[str, Any]) -> str:
        blob_id = str(uuid.uuid4())
        with open(self._path(blob_id), 'wb') as f:
            f.write(data)
        with open(self._meta_path(blob_id), 'w') as f:
            json.dump(meta, f)
        return blob_id

    def load(self, blob_id: str) -> bytes:
        with open(self._path(blob_id), 'rb') as f:
            return f.read()

    def info(self, blob_id: str) -> Dict[str, Any]:
        with open(self._meta_path(blob_id), 'r') as f:
            return json.load(f)

    def delete(self, blob_id: str) -> None:
        os.remove(self._path(blob_id))
        os.remove(self._meta_path(blob_id))

    def purge_old(self) -> None:
        current_time = time.time()
        for filename in os.listdir(self.root):
            if filename.endswith('.meta'):
                meta_path = os.path.join(self.root, filename)
                with open(meta_path, 'r') as f:
                    meta = json.load(f)
                if 'timestamp' in meta and (current_time - meta['timestamp']) > self.janitor_after_h * 3600:
                    blob_id = filename[:-5]
                    self.delete(blob_id)
