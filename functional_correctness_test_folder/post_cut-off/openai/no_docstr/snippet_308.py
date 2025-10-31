
import uuid
from collections import OrderedDict
from typing import Any, Dict


class InMemoryBlobStore:
    """
    A simple in‑memory blob store with an LRU eviction policy.
    """

    def __init__(self, max_size: int = 100):
        """
        Create a new blob store.

        Parameters
        ----------
        max_size : int, optional
            Maximum number of blobs to keep in the store. When the limit is
            exceeded, the least‑recently‑used blob is evicted. Defaults to 100.
        """
        if max_size <= 0:
            raise ValueError("max_size must be a positive integer")
        self._max_size = max_size
        # OrderedDict keeps insertion order; we will move accessed items to the end.
        self._store: "OrderedDict[str, tuple[bytes, dict[str, Any]]]" = OrderedDict(
        )

    def _evict_if_needed(self) -> None:
        """
        Evict the least‑recently‑used blob if the store exceeds its maximum size.
        """
        while len(self._store) > self._max_size:
            # popitem(last=False) removes the first item (LRU)
            evicted_id, _ = self._store.popitem(last=False)
            # For debugging or logging you could add a log statement here.

    def save(self, data: bytes, meta: Dict[str, Any]) -> str:
        """
        Store a blob and its metadata.

        Parameters
        ----------
        data : bytes
            The binary data to store.
        meta : dict[str, Any]
            Metadata associated with the blob.

        Returns
        -------
        str
            The unique identifier for the stored blob.
        """
        blob_id = uuid.uuid4().hex
        self._store[blob_id] = (data, meta)
        # Move to end to mark as most recently used
        self._store.move_to_end(blob_id)
        self._evict_if_needed()
        return blob_id

    def load(self, blob_id: str) -> bytes:
        """
        Retrieve the binary data for a given blob ID.

        Parameters
        ----------
        blob_id : str
            The identifier of the blob to load.

        Returns
        -------
        bytes
            The stored binary data.

        Raises
        ------
        KeyError
            If the blob_id does not exist in the store.
        """
        if blob_id not in self._store:
            raise KeyError(f"Blob ID {blob_id!r} not found")
        data, _ = self._store[blob_id]
        # Mark as recently used
        self._store.move_to_end(blob_id)
        return data

    def info(self, blob_id: str) -> Dict[str, Any]:
        """
        Retrieve the metadata for a given blob ID.

        Parameters
        ----------
        blob_id : str
            The identifier of the blob.

        Returns
        -------
        dict[str, Any]
            The metadata associated with the blob.

        Raises
        ------
        KeyError
            If the blob_id does not exist in the store.
        """
        if blob_id not in self._store:
            raise KeyError(f"Blob ID {blob_id!r} not found")
        _, meta = self._store[blob_id]
        # Mark as recently used
        self._store.move_to_end(blob_id)
        return meta

    def delete(self, blob_id: str) -> None:
        """
        Remove a blob and its metadata from the store.

        Parameters
        ----------
        blob_id : str
            The identifier of the blob to delete.

        Raises
        ------
        KeyError
            If the blob_id does not exist in the store.
        """
        try:
            del self._store[blob_id]
        except KeyError:
            raise KeyError(f"Blob ID {blob_id!r} not found")
