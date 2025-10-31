from typing import Any, Callable, TYPE_CHECKING

class EventContainer:
    _serializable = False
    if TYPE_CHECKING:

        @type_check_only
        def __getattr__(self, __name: str) -> Event:
            ...

        @type_check_only
        def __setattr__(self, __name: str, __value: Event) -> None:
            ...