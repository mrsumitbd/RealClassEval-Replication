
from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable, Union


class Api(ABC):

    @abstractmethod
    def call_action(self, action: str, **params) -> Union[Awaitable[Any], Any]:
        pass

    def __getattr__(self, item: str) -> Callable[..., Union[Awaitable[Any], Any]]:
        def wrapper(**kwargs):
            return self.call_action(item, **kwargs)
        return wrapper
