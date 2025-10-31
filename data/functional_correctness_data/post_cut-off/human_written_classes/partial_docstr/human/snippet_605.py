from collections import OrderedDict
from typing import final

@final
class Lookup:
    """
    Fixed-size 1-based string-to-index mapping with LRU eviction.

    - Assigns incrementing indices starting from 1.
    - After reaching the maximum size, reuses the existing indices from evicting
      the least-recently-used entries.
    - Index 0 is reserved for delta encoding in Jelly streams.

    To check if a key exists, use `.move(key)` and catch `KeyError`.
    If `KeyError` is raised, the key can be inserted with `.insert(key)`.

    Parameters
    ----------
    max_size
        Maximum number of entries. Zero disables lookup.

    """

    def __init__(self, max_size: int) -> None:
        self.data = OrderedDict[str, int]()
        self.max_size = max_size
        self._evicting = False

    def make_last_to_evict(self, key: str) -> None:
        self.data.move_to_end(key)

    def insert(self, key: str) -> int:
        if not self.max_size:
            msg = 'lookup is zero, cannot insert'
            raise IndexError(msg)
        assert key not in self.data, f'key {key!r} already present'
        if self._evicting:
            _, index = self.data.popitem(last=False)
            self.data[key] = index
        else:
            index = len(self.data) + 1
            self.data[key] = index
            self._evicting = index == self.max_size
        return index

    def __repr__(self) -> str:
        max_size, data = (self.max_size, self.data)
        return f'Lookup(max_size={max_size!r}, data={data!r})'