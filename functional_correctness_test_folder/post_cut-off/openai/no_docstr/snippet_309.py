
import json
import os
import uuid
import time
from pathlib import Path
from typing import Any, Dict, Optional


class LocalFileBlobStore:
    """
    A simple local file based blob store.

    Each blob is stored as a file named by its UUID in the root directory.
    Metadata is stored in a separate JSON file with the same name plus a
    ".meta" suffix.
    """

    def __init__(self, root: Optional[str] = None, janitor_after_h: int = 24):
        """
        Parameters
        ----------
        root : str | None
            Directory where blobs are stored. If None, a temporary directory
            is created under the system's temp folder.
        janitor_after_h : int
            Number of hours after which a blob is considered old and can be
            purged by :meth:`purge_old`.
        """
        if root is None:
            root = os.path.join(os.path.abspath(os.sep), "tmp", "blobstore")
        self.root = Path(root).expanduser().resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.janitor_after = janitor_after_h * 3600  # seconds

    def _path(self, blob_id: str) -> Path:
        """Return the Path to the data file for the given blob_id."""
        return self.root / blob_id

    def _meta_path(self, blob_id: str) -> Path:
        """Return the Path to the metadata file for the given blob_id."""
        return self.root / f"{blob_id}.meta"

    def save(self, data: bytes, meta: Dict[str, Any]) -> str:
        """
        Save a blob and its metadata.

        Parameters
        ----------
        data : bytes
            The binary data to store.
        meta : dict
            Metadata dictionary to store alongside the blob.

        Returns
        -------
        str
            The generated blob_id.
        """
        blob_id = uuid.uuid4().hex
        data_path = self._path(blob_id)
        meta_path = self._meta_path(blob_id)

        # Write data atomically
        tmp_data = data_path.with_suffix(".tmp")
        tmp_data.write_bytes(data)
        tmp_data.replace(data_path)

        # Write metadata atomically
        tmp_meta = meta_path.with_suffix(".tmp")
        tmp_meta.write_text(json.dumps(
            meta, ensure_ascii=False), encoding="utf-8")
        tmp_meta.replace(meta_path)

        return blob_id

    def load(self, blob_id: str) -> bytes:
        """
        Load the binary data for a given blob_id.

        Raises
        ------
        FileNotFoundError
            If the blob does not exist.
        """
        data_path = self._path(blob_id)
        if not data_path.is_file():
            raise FileNotFoundError(f"Blob {blob_id} not found")
        return data_path.read_bytes()

    def info(self, blob_id: str) -> Dict[str, Any]:
        """
        Retrieve the metadata for a given blob_id.

        Raises
        ------
        FileNotFoundError
            If the metadata file does not exist.
        """
        meta_path = self._meta_path(blob_id)
        if not meta_path.is_file():
            raise FileNotFoundError(f"Metadata for blob {blob_id} not found")
        return json.loads(meta_path.read_text(encoding="utf-8"))

    def delete(self, blob_id: str) -> None:
        """
        Delete both the data and metadata files for a given blob_id.
        """
        data_path = self._path(blob_id)
        meta_path = self._meta_path(blob_id)
        for path in (data_path, meta_path):
            try:
                path.unlink()
            except FileNotFoundError:
                pass

    def purge_old(self) -> None:
        """
        Delete all blobs older than `janitor_after_h` hours.
        """
        now = time.time()
        for entry in self.root.iterdir():
            if entry.is_file():
                # Skip metadata files; they will be removed with their data file
                if entry.suffix == ".meta":
                    continue
                mtime = entry.stat().st_mtime
                if now - mtime > self.janitor_after:
                    # Delete data file and its metadata
                    blob_id = entry.name
                    self.delete(blob_id)
