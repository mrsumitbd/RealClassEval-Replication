from abc import abstractmethod
from typing import Any, Callable, List, Protocol, Tuple, Type, TypeVar, Union

class BaseFormatter:
    name: str = NotImplemented
    mimetypes: Tuple[str, ...] = ()

    @abstractmethod
    def decode(self, value):
        raise NotImplementedError

    @abstractmethod
    def encode(self, value):
        raise NotImplementedError