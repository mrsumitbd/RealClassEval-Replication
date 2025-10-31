
import os
import json
import uuid
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional


class LocalFileBlobStore:
    def __init__(self, root: Optional[str] = None, janitor_after_h: int = 24):
        """
        Initialize the local file blob store.

        Args:
            root: Root directory for blob storage (defaults to env BLOB_STORE_PATH or CWD/blobs).
            janitor_after_h: Number of hours after which blobs are eligible for cleanup.
        """
        if root is None:
            root = os.getenv("BLOB_STORE_PATH")
        if not root:
            root = Path.cwd() / "blobs"
        self.root = Path(root).expanduser().resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.janitor_after = timedelta(hours=janitor_after_h)

    def _path(self, blob_id: str) -> Path:
        """Return the file path for the blob data."""
        return self.root / blob_id

    def _meta_path(self, blob_id: str) -> Path:
        """Return the file path for the blob metadata."""
        return self.root / f"{blob_id}.meta.json"

    def save(self, data: bytes, meta: Dict[str, Any]) -> str:
        """
        Save binary data and metadata to the store.

        Args:
            data: Binary data to store.
            meta: Dictionary of metadata to store.

        Returns:
            The generated blob ID.
        """
        blob_id = uuid.uuid4().hex
        data_path = self._path(blob_id)
        meta_path = self._meta_path(blob_id)

        # Write data
        with data_path.open("wb") as f:
            f.write(data)

        # Write metadata
        meta_copy = dict(meta)  # shallow copy to avoid side effects
        meta_copy["created_at"] = datetime.utcnow().isoformat()
        with meta_path.open("w", encoding="utf-8") as f:
            json.dump(meta_copy, f, ensure_ascii=False, indent=2)

        return blob_id

    def load(self, blob_id: str) -> bytes:
        """
        Load binary data by blob ID.

        Args:
            blob_id: The blob ID to load.

        Returns:
            Binary data.

        Raises:
            FileNotFoundError: If the blob doesn't exist.
        """
        data_path = self._path(blob_id)
        if not data_path.is_file():
            raise FileNotFoundError(f"Blob {blob_id} not found")
        return data_path.read_bytes()

    def info(self, blob_id: str) -> Dict[str, Any]:
        """
        Retrieve metadata for a blob.

        Args:
            blob_id: The blob ID.

        Returns:
            Metadata dictionary.

        Raises:
            FileNotFoundError: If the metadata file doesn't exist.
        """
        meta_path = self._meta_path(blob_id)
        if not meta_path.is_file():
            raise FileNotFoundError(f"Metadata for blob {blob_id} not found")
        with meta_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def delete(self, blob_id: str) -> None:
        """
        Delete a blob and its metadata.

        Args:
            blob_id: The blob ID to delete.
        """
        data_path = self._path(blob_id)
        meta_path = self._meta_path(blob_id)
        for path in (data_path, meta_path):
            try:
                path.unlink()
            except FileNotFoundError:
                pass

    def purge_old(self) -> None:
        """Remove blobs older than the janitor threshold."""
        now = datetime.utcnow()
        for entry in self.root.iterdir():
            if entry.is_file() and not entry.name.endswith(".meta.json"):
                # Check age of data file
                mtime = datetime.utcfromtimestamp(entry.stat().st_mtime)
                if now - mtime > self.janitor_after:
                    blob_id = entry.name
                    self.delete(blob_id)
