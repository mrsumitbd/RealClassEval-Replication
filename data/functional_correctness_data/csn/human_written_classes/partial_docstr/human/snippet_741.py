import hashlib
from typing import Optional, Union
import os

class DuplicatePool:
    """
    A pool that collects information about potential duplicate files.
    """

    def __init__(self):
        self._size_to_paths_map = {}
        self._size_and_hash_to_path_map = {}

    @staticmethod
    def _hash_for(path_to_hash):
        buffer_size = 1024 * 1024
        sha256_hash = hashlib.sha256()
        with open(path_to_hash, 'rb', buffer_size) as file_to_hash:
            data = file_to_hash.read(buffer_size)
            while len(data) >= 1:
                sha256_hash.update(data)
                data = file_to_hash.read(buffer_size)
        return sha256_hash.digest()

    def duplicate_path(self, source_path: str) -> Optional[str]:
        """
        Path to a duplicate for ``source_path`` or ``None`` if no duplicate exists.

        Internally information is stored to identify possible future duplicates of
        ``source_path``.
        """
        result = None
        source_size = os.path.getsize(source_path)
        paths_with_same_size = self._size_to_paths_map.get(source_size)
        if paths_with_same_size is None:
            self._size_to_paths_map[source_size] = [source_path]
        else:
            source_hash = DuplicatePool._hash_for(source_path)
            if len(paths_with_same_size) == 1:
                initial_path_with_same_size = paths_with_same_size[0]
                initial_hash = DuplicatePool._hash_for(initial_path_with_same_size)
                self._size_and_hash_to_path_map[source_size, initial_hash] = initial_path_with_same_size
            result = self._size_and_hash_to_path_map.get((source_size, source_hash))
            self._size_and_hash_to_path_map[source_size, source_hash] = source_path
        return result