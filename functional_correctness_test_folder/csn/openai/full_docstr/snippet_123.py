
import multiprocessing
from typing import Iterable, List, Optional


class MultiprocessingStringIO:
    """
    Provide a StringIO‑like interface to a multiprocessing ListProxy.
    The ListProxy must be created before the plugin is configured; it is
    stored as a class variable and can be set via the `set_shared_list`
    class method.
    """

    # Class variable that holds the shared list proxy
    _shared_list: Optional[multiprocessing.managers.ListProxy] = None

    @classmethod
    def set_shared_list(cls, shared_list: multiprocessing.managers.ListProxy) -> None:
        """
        Set the shared ListProxy that all instances will use.
        """
        cls._shared_list = shared_list

    def __init__(self, shared_list: Optional[multiprocessing.managers.ListProxy] = None):
        """
        Create a new instance. If a shared_list is provided it is used;
        otherwise the class variable is used. Raises an error if no list
        is available.
        """
        self._shared_list = shared_list or self.__class__._shared_list
        if self._shared_list is None:
            raise RuntimeError(
                "MultiprocessingStringIO: shared list not initialized")

    def getvalue(self) -> str:
        """
        Return the concatenated string stored in the shared list.
        """
        return "".join(self._shared_list)

    def writelines(self, content_list: Iterable[str]) -> None:
        """
        Append each string from `content_list` to the shared list.
        """
        self._shared_list.extend(content_list)

    def write(self, s: str) -> None:
        """
        Append a single string to the shared list.
        """
        self._shared_list.append(s)
