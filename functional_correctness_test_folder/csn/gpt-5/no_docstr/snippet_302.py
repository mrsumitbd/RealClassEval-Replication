from typing import Any, Callable, Dict, Iterable, Optional, Tuple, Type, Union


class ErrorHandler:
    def __init__(
        self,
        handlers: Optional[
            Union[
                Dict[Type[BaseException], Callable[[BaseException], Any]],
                Iterable[Tuple[Type[BaseException],
                               Callable[[BaseException], Any]]],
            ]
        ] = None,
        default: Optional[Callable[[BaseException], Any]] = None,
    ) -> None:
        self._handlers: Dict[Type[BaseException],
                             Callable[[BaseException], Any]] = {}
        if handlers:
            if isinstance(handlers, dict):
                for exc_type, func in handlers.items():
                    self.register(exc_type, func)
            else:
                for exc_type, func in handlers:
                    self.register(exc_type, func)
        self._default = default

    def register(self, exc_type: Type[BaseException], handler: Callable[[BaseException], Any]) -> None:
        if not isinstance(exc_type, type) or not issubclass(exc_type, BaseException):
            raise TypeError("exc_type must be an exception type")
        if not callable(handler):
            raise TypeError("handler must be callable")
        self._handlers[exc_type] = handler

    def unregister(self, exc_type: Type[BaseException]) -> None:
        self._handlers.pop(exc_type, None)

    def can_handle(self, e):
        if not isinstance(e, BaseException):
            return False
        return self._find_best_match(type(e)) is not None or self._default is not None

    def handle(self, e):
        if not isinstance(e, BaseException):
            raise TypeError("handle expects an exception instance")
        match = self._find_best_match(type(e))
        if match:
            handler = self._handlers[match]
            return handler(e)
        if self._default is not None:
            return self._default(e)
        raise e

    def _find_best_match(self, exc_cls: Type[BaseException]) -> Optional[Type[BaseException]]:
        best_type: Optional[Type[BaseException]] = None
        best_distance = float("inf")
        for registered in self._handlers.keys():
            if issubclass(exc_cls, registered):
                distance = self._mro_distance(exc_cls, registered)
                if distance < best_distance:
                    best_distance = distance
                    best_type = registered
        return best_type

    @staticmethod
    def _mro_distance(child: Type[BaseException], parent: Type[BaseException]) -> int:
        try:
            return child.mro().index(parent)
        except ValueError:
            return float("inf")
