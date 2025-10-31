from typing import Any, Callable, Deque, Iterator, NamedTuple, Sequence, TYPE_CHECKING, Tuple, Type, TypeVar, Union, cast, overload

class ProcessStreamAdapter:
    """Class wiring all calls to the contained Process instance.

    Use this type to hide the underlying process to provide access only to a specified
    stream. The process is usually wrapped into an :class:`~git.cmd.Git.AutoInterrupt`
    class to kill it if the instance goes out of scope.
    """
    __slots__ = ('_proc', '_stream')

    def __init__(self, process: 'Popen', stream_name: str) -> None:
        self._proc = process
        self._stream: StringIO = getattr(process, stream_name)

    def __getattr__(self, attr: str) -> Any:
        return getattr(self._stream, attr)