import os
import json
import time
import uuid
import tempfile
from typing import Any


class LocalFileBlobStore:
    def __init__(self, root: str | None = None, janitor_after_h: int = 24):
        self.root = root or os.path.join(
            tempfile.gettempdir(), "localfileblobstore")
        self.janitor_after_h = janitor_after_h
        os.makedirs(self.root, exist_ok=True)

    def _path(self, blob_id: str) -> str:
        subdir = os.path.join(self.root, blob_id[:2])
        return os.path.join(subdir, blob_id)

    def _meta_path(self, blob_id: str) -> str:
        return self._path(blob_id) + ".meta.json"

    def save(self, data: bytes, meta: dict[str, Any]) -> str:
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("data must be bytes-like")
        if meta is None:
            meta = {}
        elif not isinstance(meta, dict):
            raise TypeError("meta must be a dict")

        blob_id = uuid.uuid4().hex
        path = self._path(blob_id)
        meta_path = self._meta_path(blob_id)
        os.makedirs(os.path.dirname(path), exist_ok=True)

        tmp_data_path = path + f".tmp.{uuid.uuid4().hex}"
        with open(tmp_data_path, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_data_path, path)

        stored_meta = dict(meta)
        now = time.time()
        stored_meta.setdefault("created_at", now)
        stored_meta["size"] = len(data)
        stored_meta["blob_id"] = blob_id

        tmp_meta_path = meta_path + f".tmp.{uuid.uuid4().hex}"
        with open(tmp_meta_path, "w", encoding="utf-8") as f:
            json.dump(stored_meta, f, ensure_ascii=False,
                      separators=(",", ":"))
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_meta_path, meta_path)

        return blob_id

    def load(self, blob_id: str) -> bytes:
        path = self._path(blob_id)
        with open(path, "rb") as f:
            return f.read()

    def info(self, blob_id: str) -> dict[str, Any]:
        meta_path = self._meta_path(blob_id)
        if not os.path.exists(meta_path):
            # Fallback to minimal info from file stats if available
            path = self._path(blob_id)
            st = os.stat(path)  # raises FileNotFoundError if missing
            return {
                "blob_id": blob_id,
                "size": st.st_size,
                "created_at": st.st_mtime,
            }
        with open(meta_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def delete(self, blob_id: str) -> None:
        path = self._path(blob_id)
        meta_path = self._meta_path(blob_id)
        removed_any = False

        try:
            os.remove(path)
            removed_any = True
        except FileNotFoundError:
            pass

        try:
            os.remove(meta_path)
            removed_any = True or removed_any
        except FileNotFoundError:
            pass

        if not removed_any:
            raise FileNotFoundError(f"Blob {blob_id} not found")

    def purge_old(self) -> None:
        if self.janitor_after_h <= 0:
            return
        cutoff = time.time() - (self.janitor_after_h * 3600)
        for dirpath, _, filenames in os.walk(self.root):
            for name in filenames:
                if name.endswith(".meta.json"):
                    blob_id = name[:-10]  # remove ".meta.json"
                    meta_path = os.path.join(dirpath, name)
                    data_path = os.path.join(dirpath, blob_id)
                    try:
                        with open(meta_path, "r", encoding="utf-8") as f:
                            meta = json.load(f)
                        created_at = meta.get("created_at")
                    except Exception:
                        created_at = None

                    if created_at is None:
                        try:
                            st = os.stat(data_path)
                            created_at = st.st_mtime
                        except FileNotFoundError:
                            created_at = None

                    if created_at is not None and created_at < cutoff:
                        try:
                            os.remove(data_path)
                        except FileNotFoundError:
                            pass
                        try:
                            os.remove(meta_path)
                        except FileNotFoundError:
                            pass
                else:
                    # Consider data files without meta
                    if len(name) == 32 and all(c in "0123456789abcdef" for c in name):
                        data_path = os.path.join(dirpath, name)
                        try:
                            st = os.stat(data_path)
                            if st.st_mtime < cutoff:
                                os.remove(data_path)
                        except FileNotFoundError:
                            pass
