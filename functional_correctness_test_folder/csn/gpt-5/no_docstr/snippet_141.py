from typing import Any, Awaitable, Callable, Union
import abc


class Api(abc.ABC):

    @abc.abstractmethod
    def call_action(self, action: str, **params) -> Union[Awaitable[Any], Any]:
        raise NotImplementedError

    def __getattr__(self, item: str) -> Callable[..., Union[Awaitable[Any], Any]]:
        if item.startswith("_"):
            raise AttributeError(item)

        def _caller(*args: Any, **kwargs: Any) -> Union[Awaitable[Any], Any]:
            if args:
                if len(args) == 1 and isinstance(args[0], dict):
                    return self.call_action(item, **{**args[0], **kwargs})
                raise TypeError(
                    f"{item}() accepts only keyword arguments or a single dict positional argument")
            return self.call_action(item, **kwargs)

        return _caller
