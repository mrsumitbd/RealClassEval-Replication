
from typing import Any, Type, Dict, Tuple


class LazyField:
    """
    A lightweight wrapper that defers the creation of a Field instance until
    `create()` is called. It allows specifying positional and keyword arguments
    via the call syntax and further customization via `update()`.
    """

    def __init__(self, klass: Type[Any]) -> None:
        """
        Initialize the lazy field with the target Field class.

        Parameters
        ----------
        klass : Type[Any]
            The class that will be instantiated when `create()` is called.
        """
        self._klass: Type[Any] = klass
        self._args: Tuple[Any, ...] = ()
        self._kwargs: Dict[str, Any] = {}

    def __call__(self, *args: Any, **kwargs: Any) -> "LazyField":
        """
        Instantiate a new lazy field with the given positional and keyword
        arguments. This does not create the actual Field instance yet.

        Returns
        -------
        LazyField
            A new LazyField instance configured with the supplied arguments.
        """
        new = LazyField(self._klass)
        new._args = args
        new._kwargs = kwargs
        return new

    def update(self, **kwargs: Any) -> "LazyField":
        """
        Update the keyword arguments of the lazy field. This method mutates the
        current instance and returns it for chaining.

        Parameters
        ----------
        **kwargs : Any
            Keyword arguments to merge into the existing configuration.

        Returns
        -------
        LazyField
            The updated LazyField instance.
        """
        self._kwargs.update(kwargs)
        return self

    def create(self) -> Any:
        """
        Create the actual Field instance using the stored class, positional
        arguments, and keyword arguments.

        Returns
        -------
        Any
            An instance of the target Field class.
        """
        return self._klass(*self._args, **self._kwargs)
