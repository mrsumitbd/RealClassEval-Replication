from pipask._vendor.pip._internal.models.link import Link
import os
from typing import Any, Dict, List, Optional
from packaging.tags import Tag, interpreter_name, interpreter_version

class Cache:
    """An abstract class - provides cache directories for data from links

    :param cache_dir: The root of the cache.
    """

    def __init__(self, cache_dir: str) -> None:
        super().__init__()
        assert not cache_dir or os.path.isabs(cache_dir)
        self.cache_dir = cache_dir or None

    def _get_cache_path_parts(self, link: Link) -> List[str]:
        """Get parts of part that must be os.path.joined with cache_dir"""
        key_parts = {'url': link.url_without_fragment}
        if link.hash_name is not None and link.hash is not None:
            key_parts[link.hash_name] = link.hash
        if link.subdirectory_fragment:
            key_parts['subdirectory'] = link.subdirectory_fragment
        key_parts['interpreter_name'] = interpreter_name()
        key_parts['interpreter_version'] = interpreter_version()
        hashed = _hash_dict(key_parts)
        parts = [hashed[:2], hashed[2:4], hashed[4:6], hashed[6:]]
        return parts

    def _get_candidates(self, link: Link, canonical_package_name: str) -> List[Any]:
        can_not_cache = not self.cache_dir or not canonical_package_name or (not link)
        if can_not_cache:
            return []
        path = self.get_path_for_link(link)
        if os.path.isdir(path):
            return [(candidate, path) for candidate in os.listdir(path)]
        return []

    def get_path_for_link(self, link: Link) -> str:
        """Return a directory to store cached items in for link."""
        raise NotImplementedError()

    def get(self, link: Link, package_name: Optional[str], supported_tags: List[Tag]) -> Link:
        """Returns a link to a cached item if it exists, otherwise returns the
        passed link.
        """
        raise NotImplementedError()