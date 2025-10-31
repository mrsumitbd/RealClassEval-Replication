from typing import Any, Callable, Dict, Generator, List, Optional, TypeVar, Union

class TempDirectoryTypeRegistry:
    """Manages temp directory behavior"""

    def __init__(self) -> None:
        self._should_delete: Dict[str, bool] = {}

    def set_delete(self, kind: str, value: bool) -> None:
        """Indicate whether a TempDirectory of the given kind should be
        auto-deleted.
        """
        self._should_delete[kind] = value

    def get_delete(self, kind: str) -> bool:
        """Get configured auto-delete flag for a given TempDirectory type,
        default True.
        """
        return self._should_delete.get(kind, True)