from abc import ABC, abstractmethod
from typing import Any


class SessionListener(ABC):
    '''Base class for :class:`Session` listeners, which are notified when a new
    NETCONF message is received or an error occurs.
    .. note::
        Avoid time-intensive tasks in a callback's context.
    '''

    @abstractmethod
    def callback(self, root: Any, raw: Any) -> None:
        pass

    @abstractmethod
    def errback(self, ex: Exception) -> None:
        '''Called when an error occurs.
        :type ex: :exc:`Exception`
        '''
        pass
