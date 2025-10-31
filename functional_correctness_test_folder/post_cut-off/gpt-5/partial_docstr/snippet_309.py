from __future__ import annotations

import json
import os
import shutil
import uuid
import hashlib
from datetime import datetime, timezone, timedelta
from typing import Any


class LocalFileBlobStore:
    def __init__(self, root: str | None = None, janitor_after_h: int = 24):
        '''
        Initialize the local file blob store.
        Args:
            root: Root directory for blob storage (defaults to env BLOB_STORE_PATH or CWD/blobs).            janitor_after_h: Number of hours after which blobs are eligible for cleanup
        '''
        root = root or os.getenv(
            "BLOB_STORE_PATH") or os.path.join(os.getcwd(), "blobs")
        self.root = os.path.abspath(root)
        self.janitor_after_h = int(janitor_after_h)
        os.makedirs(self.root, exist_ok=True)

    def _path(self, blob_id: str) -> str:
        return os.path.join(self.root, f"{blob_id}.bin")

    def _meta_path(self, blob_id: str) -> str:
        return os.path.join(self.root, f"{blob_id}.json")

    def save(self, data: bytes, meta: dict[str, Any]) -> str:
        blob_id = uuid.uuid4().hex
        data_path = self._path(blob_id)
        meta_path = self._meta_path(blob_id)

        sha256 = hashlib.sha256(data).hexdigest()
        created_at = datetime.now(timezone.utc).isoformat()

        full_meta = {
            "id": blob_id,
            "created_at": created_at,
            "size": len(data),
            "sha256": sha256,
            "user_meta": meta or {},
        }

        tmp_data = data_path + ".tmp"
        tmp_meta = meta_path + ".tmp"

        os.makedirs(self.root, exist_ok=True)
        with open(tmp_data, "wb") as f:
            f.write(data)
        os.replace(tmp_data, data_path)

        with open(tmp_meta, "w", encoding="utf-8") as f:
            json.dump(full_meta, f, ensure_ascii=False,
                      indent=2, sort_keys=True)
        os.replace(tmp_meta, meta_path)

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
        path = self._path(blob_id)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Blob not found: {blob_id}")
        with open(path, "rb") as f:
            return f.read()

    def info(self, blob_id: str) -> dict[str, Any]:
        meta_path = self._meta_path(blob_id)
        data_path = self._path(blob_id)

        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Blob not found: {blob_id}")

        info: dict[str, Any] = {"id": blob_id}

        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as f:
                stored = json.load(f)
            info.update(stored)
        else:
            stat = os.stat(data_path)
            info.update(
                {
                    "size": stat.st_size,
                    "created_at": datetime.fromtimestamp(stat.st_ctime, tz=timezone.utc).isoformat(),
                    "user_meta": {},
                }
            )

        # Add filesystem timestamps
        stat = os.stat(data_path)
        info["mtime"] = datetime.fromtimestamp(
            stat.st_mtime, tz=timezone.utc).isoformat()
        info["atime"] = datetime.fromtimestamp(
            stat.st_atime, tz=timezone.utc).isoformat()
        info["path"] = data_path
        return info

    def delete(self, blob_id: str) -> None:
        data_path = self._path(blob_id)
        meta_path = self._meta_path(blob_id)

        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Blob not found: {blob_id}")

        try:
            os.remove(data_path)
        finally:
            # Remove meta if present
            if os.path.exists(meta_path):
                try:
                    os.remove(meta_path)
                except Exception:
                    pass

    def purge_old(self) -> None:
        '''Remove blobs older than the janitor threshold.'''
        threshold = datetime.now(timezone.utc) - \
            timedelta(hours=self.janitor_after_h)

        for entry in os.scandir(self.root):
            if not entry.is_file():
                continue

            if entry.name.endswith(".json"):
                blob_id = entry.name[:-5]
                data_path = self._path(blob_id)
                meta_path = entry.path

                # Determine created_at
                created_at_dt: datetime | None = None
                try:
                    with open(meta_path, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                    ca = meta.get("created_at")
                    if isinstance(ca, str):
                        try:
                            created_at_dt = datetime.fromisoformat(
                                ca.replace("Z", "+00:00"))
                        except Exception:
                            created_at_dt = None
                except Exception:
                    created_at_dt = None

                if created_at_dt is None:
                    # Fallback to data file mtime if exists, else meta mtime
                    ref_path = data_path if os.path.exists(
                        data_path) else meta_path
                    try:
                        st = os.stat(ref_path)
                        created_at_dt = datetime.fromtimestamp(
                            st.st_mtime, tz=timezone.utc)
                    except Exception:
                        created_at_dt = None

                if created_at_dt is None:
                    continue

                if created_at_dt <= threshold:
                    # Delete data and meta
                    if os.path.exists(data_path):
                        try:
                            os.remove(data_path)
                        except Exception:
                            pass
                    try:
                        os.remove(meta_path)
                    except Exception:
                        pass

        # Also handle orphan .bin files without .json
        for entry in os.scandir(self.root):
            if not entry.is_file() or not entry.name.endswith(".bin"):
                continue
            blob_id = entry.name[:-4]
            meta_path = self._meta_path(blob_id)
            if os.path.exists(meta_path):
                continue
            try:
                st = os.stat(entry.path)
                mtime = datetime.fromtimestamp(st.st_mtime, tz=timezone.utc)
                if mtime <= threshold:
                    os.remove(entry.path)
            except Exception:
                pass
