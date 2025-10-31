
from abc import abstractmethod
from typing import Any, Awaitable, Callable, Union


class Api:

    @abstractmethod
    def call_action(self, action: str, **params) -> Union[Awaitable[Any], Any]:
        pass

    def __getattr__(self, item: str) -> Callable[..., Union[Awaitable[Any], Any]]:
        def method(**kwargs):
            return self.call_action(item, **kwargs)
        return method
