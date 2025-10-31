from typing import Any, Optional, Type
from types import TracebackType

class NoLock:
    """
    A dummy context manager that raises a RuntimeError when it's used. This makes it easier to
    detect cases where an :class:`Adapter` has not received the proper lock-object to make sure
    that device/interface access is synchronous.
    """

    def __enter__(self) -> None:
        raise RuntimeError('The attempted action requires a proper threading.Lock-object, but none was available.')

    def __exit__(self, exctype: Optional[Type[BaseException]], excinst: Optional[BaseException], exctb: Optional[TracebackType]) -> None:
        pass