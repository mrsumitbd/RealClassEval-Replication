import os
import json
import time
import hashlib
import tempfile
from typing import Any


class LocalFileBlobStore:
    """File-based blob storage implementation."""

    def __init__(self, root: str | None = None, janitor_after_h: int = 24):
        """
        Initialize the local file blob store.
        Args:
            root: Root directory for blob storage (defaults to env BLOB_STORE_PATH or CWD/blobs).
            janitor_after_h: Number of hours after which blobs are eligible for cleanup
        """
        root = root or os.environ.get(
            "BLOB_STORE_PATH") or os.path.join(os.getcwd(), "blobs")
        self.root = os.path.abspath(root)
        self.data_root = os.path.join(self.root, "data")
        self.meta_root = os.path.join(self.root, "meta")
        self.janitor_after_h = int(janitor_after_h)
        os.makedirs(self.data_root, exist_ok=True)
        os.makedirs(self.meta_root, exist_ok=True)

    def _path(self, blob_id: str) -> str:
        """Get the file path for a blob's binary data."""
        shard1 = blob_id[:2] if len(blob_id) >= 2 else blob_id
        shard2 = blob_id[2:4] if len(blob_id) >= 4 else ""
        base = os.path.join(self.data_root, shard1)
        if shard2:
            base = os.path.join(base, shard2)
        return os.path.join(base, f"{blob_id}.bin")

    def _meta_path(self, blob_id: str) -> str:
        """Get the file path for a blob's metadata."""
        shard1 = blob_id[:2] if len(blob_id) >= 2 else blob_id
        shard2 = blob_id[2:4] if len(blob_id) >= 4 else ""
        base = os.path.join(self.meta_root, shard1)
        if shard2:
            base = os.path.join(base, shard2)
        return os.path.join(base, f"{blob_id}.json")

    def save(self, data: bytes, meta: dict[str, Any]) -> str:
        """
        Save binary data with metadata.
        Args:
            data: Binary data to store
            meta: Metadata dictionary
        Returns:
            Unique blob ID for the stored data
        """
        blob_id = hashlib.sha256(data).hexdigest()
        bpath = self._path(blob_id)
        mpath = self._meta_path(blob_id)

        os.makedirs(os.path.dirname(bpath), exist_ok=True)
        os.makedirs(os.path.dirname(mpath), exist_ok=True)

        if not os.path.exists(bpath):
            tmp_fd, tmp_path = tempfile.mkstemp(dir=os.path.dirname(bpath))
            try:
                with os.fdopen(tmp_fd, "wb") as f:
                    f.write(data)
                    f.flush()
                    os.fsync(f.fileno())
                os.replace(tmp_path, bpath)
            except Exception:
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass
                raise

        now = int(time.time())
        record: dict[str, Any]
        if os.path.exists(mpath):
            try:
                with open(mpath, "r", encoding="utf-8") as f:
                    record = json.load(f)
            except Exception:
                record = {}
        else:
            record = {}

        sys_meta = record.get("sys", {})
        if "created_at" not in sys_meta:
            sys_meta["created_at"] = now
        sys_meta["updated_at"] = now
        sys_meta["size"] = len(data)
        record["sys"] = sys_meta

        user_meta = record.get("meta", {})
        if isinstance(user_meta, dict):
            user_meta.update(meta or {})
        else:
            user_meta = dict(meta or {})
        record["meta"] = user_meta
        record["id"] = blob_id

        tmp_fd, tmp_path = tempfile.mkstemp(dir=os.path.dirname(mpath))
        try:
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
                json.dump(record, f, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_path, mpath)
        except Exception:
            try:
                os.unlink(tmp_path)
            except OSError:
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
        bpath = self._path(blob_id)
        if not os.path.exists(bpath):
            raise FileNotFoundError(f"Blob not found: {blob_id}")
        with open(bpath, "rb") as f:
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
        bpath = self._path(blob_id)
        mpath = self._meta_path(blob_id)
        if not os.path.exists(bpath) or not os.path.exists(mpath):
            raise FileNotFoundError(f"Blob not found: {blob_id}")
        with open(mpath, "r", encoding="utf-8") as f:
            return json.load(f)

    def delete(self, blob_id: str) -> None:
        """
        Delete a blob and its metadata.
        Args:
            blob_id: The blob ID to delete
        """
        bpath = self._path(blob_id)
        mpath = self._meta_path(blob_id)
        try:
            if os.path.exists(bpath):
                os.remove(bpath)
        except OSError:
            pass
        try:
            if os.path.exists(mpath):
                os.remove(mpath)
        except OSError:
            pass

    def purge_old(self) -> None:
        """Remove blobs older than the janitor threshold."""
        cutoff = int(time.time()) - self.janitor_after_h * 3600

        for root, _, files in os.walk(self.meta_root):
            for fname in files:
                if not fname.endswith(".json"):
                    continue
                mpath = os.path.join(root, fname)
                blob_id = fname[:-5]  # strip .json
                created_at = None
                try:
                    with open(mpath, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                    sys_meta = meta.get("sys", {})
                    created_at = sys_meta.get(
                        "created_at") or meta.get("created_at")
                except Exception:
                    created_at = None

                if created_at is None:
                    try:
                        created_at = int(os.path.getmtime(mpath))
                    except OSError:
                        created_at = None

                if created_at is not None and created_at <= cutoff:
                    self.delete(blob_id)
