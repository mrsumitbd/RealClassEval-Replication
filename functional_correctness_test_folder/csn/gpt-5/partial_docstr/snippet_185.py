from abc import ABC, abstractmethod
from typing import Any


class Transport(ABC):
    '''
    The transport interface.
    '''

    def __init__(self) -> None:
        '''
        Constructor.
        '''
        super().__init__()

    @abstractmethod
    def open(self, request: Any) -> None:
        pass

    @abstractmethod
    def send(self, request: Any) -> Any:
        pass
