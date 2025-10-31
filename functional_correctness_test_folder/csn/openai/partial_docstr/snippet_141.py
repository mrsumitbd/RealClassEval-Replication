
import abc
from typing import Any, Awaitable, Callable, Union


class Api(abc.ABC):
    """
    Base class for OneBot API wrappers.

    Subclasses must implement :meth:`call_action`.  The :meth:`__getattr__`
    method automatically creates a callable for any API action name.
    """

    @abc.abstractmethod
    def call_action(
        self, action: str, **params
    ) -> Union[Awaitable[Any], Any]:
        """
        调用 OneBot API，`action` 为要调用的 API 动作名，`**params`
        为 API 所需参数。
        根据实现类的不同，此函数可能是异步也可能是同步函数。
        """
        pass

    def __getattr__(self, item: str) -> Callable[..., Union[Awaitable[Any], Any]]:
        """
        Dynamically create a method for any API action.

        Example:
            api.get_status()  # calls api.call_action('get_status')
        """
        def _action(*args, **kwargs):
            # OneBot APIs are keyword‑only; positional args are ignored.
            return self.call_action(item, **kwargs)

        return _action
