
import abc
from typing import Any, Awaitable, Callable, Union


class Api(abc.ABC):
    @abc.abstractmethod
    def call_action(self, action: str, **params) -> Union[Awaitable[Any], Any]:
        """Execute the given action with the provided parameters."""
        ...

    def __getattr__(self, item: str) -> Callable[..., Union[Awaitable[Any], Any]]:
        """Return a callable that forwards to `call_action` with the attribute name as the action."""
        def _action(**params: Any) -> Union[Awaitable[Any], Any]:
            return self.call_action(item, **params)

        return _action
