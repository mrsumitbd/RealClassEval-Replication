
import abc
from typing import Any, Awaitable, Callable, Union


class Api(abc.ABC):

    @abc.abstractmethod
    def call_action(self, action: str, **params) -> Union[Awaitable[Any], Any]:
        pass

    def __getattr__(self, item: str) -> Callable[..., Union[Awaitable[Any], Any]]:
        def wrapper(*args, **kwargs):
            return self.call_action(item, *args, **kwargs)
        return wrapper
