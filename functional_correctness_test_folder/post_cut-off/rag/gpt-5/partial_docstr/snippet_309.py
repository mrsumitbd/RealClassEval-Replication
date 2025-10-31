import os
import json
import time
import secrets
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
        root_dir = root or os.environ.get(
            "BLOB_STORE_PATH") or os.path.join(os.getcwd(), "blobs")
        self._root = os.path.abspath(root_dir)
        self._janitor_after_s = int(janitor_after_h * 3600)
        os.makedirs(self._root, exist_ok=True)

    def _safe_blob_id(self, blob_id: str) -> str:
        if not blob_id or blob_id in (".", ".."):
            raise ValueError("Invalid blob id")
        if os.sep in blob_id:
            raise ValueError("Invalid blob id: contains path separator")
        if os.altsep and os.altsep in blob_id:
            raise ValueError(
                "Invalid blob id: contains alternate path separator")
        return blob_id

    def _path(self, blob_id: str) -> str:
        """Get the file path for a blob's binary data."""
        self._safe_blob_id(blob_id)
        return os.path.join(self._root, f"{blob_id}.bin")

    def _meta_path(self, blob_id: str) -> str:
        """Get the file path for a blob's metadata."""
        self._safe_blob_id(blob_id)
        return os.path.join(self._root, f"{blob_id}.json")

    def save(self, data: bytes, meta: dict[str, Any]) -> str:
        """
        Save binary data with metadata.
        Args:
            data: Binary data to store
            meta: Metadata dictionary
        Returns:
            Unique blob ID for the stored data
        """
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("data must be bytes")
        base_id = secrets.token_hex(16)
        blob_id = base_id
        # Ensure uniqueness
        while os.path.exists(self._path(blob_id)) or os.path.exists(self._meta_path(blob_id)):
            blob_id = f"{base_id}-{secrets.token_hex(4)}"

        data_path = self._path(blob_id)
        meta_path = self._meta_path(blob_id)

        # Write data atomically
        fd_data, tmp_data = tempfile.mkstemp(
            dir=self._root, prefix="._", suffix=".bin")
        try:
            with os.fdopen(fd_data, "wb") as f:
                f.write(data)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_data, data_path)
        finally:
            try:
                if os.path.exists(tmp_data):
                    os.remove(tmp_data)
            except OSError:
                pass

        # Prepare and write metadata atomically
        meta_to_store: dict[str, Any] = dict(meta or {})
        meta_to_store.setdefault("created_at", time.time())
        meta_to_store.setdefault("size", len(data))
        meta_to_store.setdefault("id", blob_id)

        fd_meta, tmp_meta = tempfile.mkstemp(
            dir=self._root, prefix="._", suffix=".json")
        try:
            with os.fdopen(fd_meta, "w", encoding="utf-8") as f:
                json.dump(meta_to_store, f, ensure_ascii=False,
                          separators=(",", ":"))
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_meta, meta_path)
        finally:
            try:
                if os.path.exists(tmp_meta):
                    os.remove(tmp_meta)
            except OSError:
                pass

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
        data_path = self._path(blob_id)
        meta_path = self._meta_path(blob_id)
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Blob not found: {blob_id}")

        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
            return meta

        st = os.stat(data_path)
        return {
            "id": blob_id,
            "size": st.st_size,
            "created_at": st.st_mtime,
        }

    def delete(self, blob_id: str) -> None:
        """
        Delete a blob and its metadata.
        Args:
            blob_id: The blob ID to delete
        """
        for p in (self._path(blob_id), self._meta_path(blob_id)):
            try:
                os.remove(p)
            except FileNotFoundError:
                pass

    def purge_old(self) -> None:
        """Remove blobs older than the janitor threshold."""
        cutoff = time.time() - self._janitor_after_s
        try:
            with os.scandir(self._root) as it:
                for entry in it:
                    if not entry.is_file():
                        continue
                    name = entry.name
                    if name.endswith(".json"):
                        blob_id = name[:-5]
                        # Prefer created_at from metadata, fallback to file mtime
                        created_at = None
                        try:
                            with open(entry.path, "r", encoding="utf-8") as f:
                                meta = json.load(f)
                            created_at = float(
                                meta.get("created_at", entry.stat().st_mtime))
                        except Exception:
                            created_at = entry.stat().st_mtime
                        if created_at <= cutoff:
                            self.delete(blob_id)
                    elif name.endswith(".bin"):
                        blob_id = name[:-4]
                        meta_path = self._meta_path(blob_id)
                        if not os.path.exists(meta_path):
                            # No metadata; rely on data file mtime
                            try:
                                st = os.stat(entry.path)
                                if st.st_mtime <= cutoff:
                                    self.delete(blob_id)
                            except FileNotFoundError:
                                pass
        except FileNotFoundError:
            pass
