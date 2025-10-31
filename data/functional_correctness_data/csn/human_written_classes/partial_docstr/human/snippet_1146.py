import inspect
import typing

class ResourceComputer:
    """
    Decorates ``computer``, a resource computing function with metadata about that function.

    Parameters
    ----------
    computer
        The function that computes the resources.
    returns
        The names of the resources that ``computer`` returns, specified in the same order as ``computer`` returns
        them.
    argmap
        A custom map of ``computer``'s argument names to the global resource names that will be passed as
        ``computer``'s arguments when ``computer`` is called.
    """

    def __init__(self, computer: typing.Callable, returns: typing.Sequence[str], argmap: typing.Mapping[str, typing.Any]=None) -> None:
        argspec = inspect.getfullargspec(computer)
        if argspec.varargs is not None or argspec.varkw is not None or argspec.defaults is not None or (len(argspec.kwonlyargs) > 0):
            raise ValueError('`computer` must use only positional arguments with no default values')
        self.computer: typing.Callable = computer
        self.returns: typing.Sequence[str] = returns
        self.argmap = {arg_name: arg_name for arg_name in argspec.args}
        if argmap is not None:
            self.argmap.update(argmap)

    def __call__(self, *args, **kwargs):
        """
        Allows a ``ResourceComputer`` instance to be callable. Just forwards all arguments on to self.computer.
        """
        return self.computer(*args, **kwargs)

    @property
    def name(self) -> str:
        """Returns the function name of self.computer"""
        return self.computer.__name__