import json
import os
import time
import uuid
import hashlib
from typing import Any


class LocalFileBlobStore:
    """File-based blob storage implementation."""

    def __init__(self, root: str | None = None, janitor_after_h: int = 24):
        """
        Initialize the local file blob store.
        Args:
            root: Root directory for blob storage (defaults to env BLOB_STORE_PATH or CWD/blobs).            janitor_after_h: Number of hours after which blobs are eligible for cleanup
        """
        base = root or os.environ.get(
            "BLOB_STORE_PATH") or os.path.join(os.getcwd(), "blobs")
        self.root = os.path.abspath(base)
        self.data_root = os.path.join(self.root, "data")
        self.meta_root = os.path.join(self.root, "meta")
        self.janitor_after_s = int(janitor_after_h * 3600)
        os.makedirs(self.data_root, exist_ok=True)
        os.makedirs(self.meta_root, exist_ok=True)

    def _shard_dirs(self, blob_id: str) -> tuple[str, str]:
        a = blob_id[0:2] if len(blob_id) >= 2 else "xx"
        b = blob_id[2:4] if len(blob_id) >= 4 else "yy"
        return a, b

    def _path(self, blob_id: str) -> str:
        """Get the file path for a blob's binary data."""
        a, b = self._shard_dirs(blob_id)
        return os.path.join(self.data_root, a, b, blob_id)

    def _meta_path(self, blob_id: str) -> str:
        """Get the file path for a blob's metadata."""
        a, b = self._shard_dirs(blob_id)
        return os.path.join(self.meta_root, a, b, f"{blob_id}.json")

    def _ensure_parents(self, path: str) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)

    def save(self, data: bytes, meta: dict[str, Any]) -> str:
        """
        Save binary data with metadata.
        Args:
            data: Binary data to store
            meta: Metadata dictionary
        Returns:
            Unique blob ID for the stored data
        """
        rng = uuid.uuid4().bytes
        content_hash = hashlib.sha256(data).hexdigest()
        blob_id = hashlib.sha256(rng + data).hexdigest()
        data_path = self._path(blob_id)
        meta_path = self._meta_path(blob_id)
        self._ensure_parents(data_path)
        self._ensure_parents(meta_path)

        # Write data atomically
        tmp_data = f"{data_path}.tmp.{uuid.uuid4().hex}"
        with open(tmp_data, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_data, data_path)

        created_at = time.time()
        meta_record: dict[str, Any] = {
            "id": blob_id,
            "size": len(data),
            "sha256": content_hash,
            "created_at": created_at,
            "meta": dict(meta) if meta is not None else {},
        }

        # Write metadata atomically
        try:
            tmp_meta = f"{meta_path}.tmp.{uuid.uuid4().hex}"
            with open(tmp_meta, "w", encoding="utf-8") as f:
                json.dump(meta_record, f, ensure_ascii=False,
                          separators=(",", ":"))
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_meta, meta_path)
        except Exception:
            try:
                os.remove(data_path)
            except FileNotFoundError:
                pass
            raise

        return blob_id

    def load(self, blob_id: str) -> bytes:
        """
        Load binary data by blob ID.
        Args:
            blob_id: The blob ID to load
        Returns:
            Binary data
        Raises:
            FileNotFoundError: If the blob doesn't exist
        """
        path = self._path(blob_id)
        with open(path, "rb") as f:
            return f.read()

    def info(self, blob_id: str) -> dict[str, Any]:
        """
        Get metadata for a blob.
        Args:
            blob_id: The blob ID
        Returns:
            Metadata dictionary
        Raises:
            FileNotFoundError: If the blob doesn't exist
        """
        mpath = self._meta_path(blob_id)
        with open(mpath, "r", encoding="utf-8") as f:
            return json.load(f)

    def delete(self, blob_id: str) -> None:
        """
        Delete a blob and its metadata.
        Args:
            blob_id: The blob ID to delete
        """
        paths = [self._path(blob_id), self._meta_path(blob_id)]
        for p in paths:
            try:
                os.remove(p)
            except FileNotFoundError:
                pass

    def purge_old(self) -> None:
        """Remove blobs older than the janitor threshold."""
        cutoff = time.time() - self.janitor_after_s

        # Walk metadata tree, decide age based on created_at or mtime
        for root, _, files in os.walk(self.meta_root):
            for fname in files:
                if not fname.endswith(".json"):
                    continue
                mpath = os.path.join(root, fname)
                try:
                    created_at: float | None = None
                    try:
                        with open(mpath, "r", encoding="utf-8") as f:
                            data = json.load(f)
                        created_at = float(data.get("created_at", 0)) if isinstance(
                            data, dict) else None
                    except Exception:
                        created_at = None
                    if created_at is None or created_at <= 0:
                        created_at = os.path.getmtime(mpath)
                    if created_at < cutoff:
                        blob_id = fname[:-5]
                        self.delete(blob_id)
                except FileNotFoundError:
                    continue
                except Exception:
                    continue
