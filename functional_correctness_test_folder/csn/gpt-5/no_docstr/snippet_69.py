from abc import ABC, abstractmethod
from typing import Any


class BaseStorage(ABC):
    @abstractmethod
    def write(self, id: Any, data: bytes) -> None:
        pass

    @abstractmethod
    def exists(self, id: Any) -> bool:
        pass

    @abstractmethod
    def max_file_idx(self) -> int:
        pass
