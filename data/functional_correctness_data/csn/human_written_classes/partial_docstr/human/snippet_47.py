from typing import Any, BinaryIO, NamedTuple, TypeVar, Union, cast

class State:
    """
    An object that can be used to store arbitrary state.

    Used for `request.state` and `app.state`.
    """
    _state: dict[str, Any]

    def __init__(self, state: dict[str, Any] | None=None):
        if state is None:
            state = {}
        super().__setattr__('_state', state)

    def __setattr__(self, key: Any, value: Any) -> None:
        self._state[key] = value

    def __getattr__(self, key: Any) -> Any:
        try:
            return self._state[key]
        except KeyError:
            message = "'{}' object has no attribute '{}'"
            raise AttributeError(message.format(self.__class__.__name__, key))

    def __delattr__(self, key: Any) -> None:
        del self._state[key]