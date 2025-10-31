from typing import Dict, Optional, List, Any, Tuple, Mapping, Collection, Union, BinaryIO
from collections.abc import Collection as CCollection
from collections.abc import Mapping as CMapping

class MessageCommand:
    """
    A message command.

    This object records a way to call a method in the module object.
    In case where the message has an :attr:`~.Message.author` from a different
    module from the :attr:`~.Message.chat`, this function MUST be called on
    the :attr:`~.Message.author`’s module.

    The method specified MUST return either a ``str`` as result or ``None``
    if this message will be edited or deleted for further interactions.

    Attributes:
        name (str): Human-friendly name of the command.
        callable_name (str): Callable name of the command.
        args (Collection[Any]): Arguments passed to the function.
        kwargs (Mapping[str, Any]): Keyword arguments passed to the function.
    """
    name: str = ''
    callable_name: str = ''
    args: Tuple = tuple()
    kwargs: Mapping[str, Any] = {}

    def __init__(self, name: str, callable_name: str, args: Collection[Any]=None, kwargs: Optional[Mapping[str, Any]]=None):
        """
        Args:
            name (str): Human-friendly name of the command.
            callable_name (str): Callable name of the command.
            args (Optional[Collection[Any]]): Arguments passed to the function. Defaulted to empty list;
            kwargs (Optional[Mapping[str, Any]]): Keyword arguments passed to the function.
                Defaulted to empty dict.
        """
        self.name = name
        self.callable_name = callable_name
        if args is not None:
            self.args = tuple(args)
        if kwargs is not None:
            self.kwargs = dict(kwargs)
        self.verify()

    def __str__(self):
        return '<MessageCommand: {name}, {callable_name}({params})>'.format(name=self.name, callable_name=self.callable_name, params=', '.join(self.args + tuple(('%r=%r' % i for i in self.kwargs.items()))))

    def verify(self):
        assert isinstance(self.name, str) and self.name, f'name {self.name!r} must be a non-empty string.'
        assert isinstance(self.callable_name, str) and self.callable_name, f'callable {self.callable_name!r} must be a non-empty string.'
        assert isinstance(self.args, CCollection), f'args {self.args!r} must be a collection.'
        assert isinstance(self.kwargs, CMapping), f'kwargs {self.kwargs!r} must be a mapping.'