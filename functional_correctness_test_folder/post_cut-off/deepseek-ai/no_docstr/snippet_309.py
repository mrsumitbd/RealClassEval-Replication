
import os
import json
import uuid
import time
from typing import Any, Dict
import shutil


class LocalFileBlobStore:

    def __init__(self, root: str | None = None, janitor_after_h: int = 24):
        self.root = root if root is not None else os.path.join(
            os.getcwd(), "blob_store")
        self.janitor_after_h = janitor_after_h
        os.makedirs(self.root, exist_ok=True)

    def _path(self, blob_id: str) -> str:
        return os.path.join(self.root, f"{blob_id}.bin")

    def _meta_path(self, blob_id: str) -> str:
        return os.path.join(self.root, f"{blob_id}.meta")

    def save(self, data: bytes, meta: Dict[str, Any]) -> str:
        blob_id = str(uuid.uuid4())
        data_path = self._path(blob_id)
        meta_path = self._meta_path(blob_id)

        with open(data_path, "wb") as f:
            f.write(data)

        meta["timestamp"] = time.time()
        with open(meta_path, "w") as f:
            json.dump(meta, f)

        return blob_id

    def load(self, blob_id: str) -> bytes:
        data_path = self._path(blob_id)
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Blob {blob_id} not found")

        with open(data_path, "rb") as f:
            return f.read()

    def info(self, blob_id: str) -> Dict[str, Any]:
        meta_path = self._meta_path(blob_id)
        if not os.path.exists(meta_path):
            raise FileNotFoundError(f"Metadata for blob {blob_id} not found")

        with open(meta_path, "r") as f:
            return json.load(f)

    def delete(self, blob_id: str) -> None:
        data_path = self._path(blob_id)
        meta_path = self._meta_path(blob_id)

        if os.path.exists(data_path):
            os.remove(data_path)
        if os.path.exists(meta_path):
            os.remove(meta_path)

    def purge_old(self) -> None:
        current_time = time.time()
        for filename in os.listdir(self.root):
            if filename.endswith(".meta"):
                blob_id = filename[:-5]
                meta_path = self._meta_path(blob_id)
                try:
                    with open(meta_path, "r") as f:
                        meta = json.load(f)
                    timestamp = meta.get("timestamp", 0)
                    if (current_time - timestamp) > (self.janitor_after_h * 3600):
                        self.delete(blob_id)
                except (json.JSONDecodeError, FileNotFoundError):
                    continue
