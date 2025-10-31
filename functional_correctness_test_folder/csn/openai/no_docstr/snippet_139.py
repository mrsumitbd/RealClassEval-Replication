
from typing import Any, Type


class LazyField:
    """
    A helper that defers the creation of a Field instance until `create` is called.
    It stores the field class, positional arguments, and keyword arguments.
    """

    def __init__(self, klass: Type[Any]) -> None:
        """
        Initialize with the field class to instantiate later.

        :param klass: The class of the field to be created.
        """
        self._klass = klass
        self._args: tuple[Any, ...] = ()
        self._kwargs: dict[str, Any] = {}

    def __call__(self, *args: Any, **kwargs: Any) -> "LazyField":
        """
        Store positional and keyword arguments for the field.

        :param args: Positional arguments for the field constructor.
        :param kwargs: Keyword arguments for the field constructor.
        :return: Self, to allow chaining.
        """
        self._args = args
        self._kwargs.update(kwargs)
        return self

    def update(self, **kwargs: Any) -> "LazyField":
        """
        Update or add keyword arguments for the field.

        :param kwargs: Keyword arguments to merge into the existing ones.
        :return: Self, to allow chaining.
        """
        self._kwargs.update(kwargs)
        return self

    def create(self) -> Any:
        """
        Instantiate and return the field using the stored class, args, and kwargs.

        :return: An instance of the field class.
        """
        return self._klass(*self._args, **self._kwargs)
