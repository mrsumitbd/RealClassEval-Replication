from abc import ABC, abstractmethod
from typing import Dict, Tuple


class SessionListener(ABC):
    '''Base class for :class:`Session` listeners, which are notified when a new
    NETCONF message is received or an error occurs.
    .. note::
        Avoid time-intensive tasks in a callback's context.
    '''

    __slots__ = ()

    @abstractmethod
    def callback(self, root: Tuple[str, Dict[str, str]], raw: str) -> None:
        '''Called when a new XML document is received. The *root* argument allows the callback to determine whether it wants to further process the document.
        Here, *root* is a tuple of *(tag, attributes)* where *tag* is the qualified name of the root element and *attributes* is a dictionary of its attributes (also qualified names).
        *raw* will contain the XML document as a string.
        '''
        raise NotImplementedError

    @abstractmethod
    def errback(self, ex: Exception) -> None:
        '''Called when an error occurs.
        :type ex: :exc:`Exception`
        '''
        raise NotImplementedError
