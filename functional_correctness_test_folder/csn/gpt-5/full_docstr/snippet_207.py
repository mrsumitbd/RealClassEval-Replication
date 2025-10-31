from abc import ABC, abstractmethod
from typing import Any, Optional


class IJavaStreamParser(ABC):
    '''
    API of the Java stream parser
    '''

    @abstractmethod
    def run(self) -> Any:
        '''
        Parses the input stream
        '''
        raise NotImplementedError

    @abstractmethod
    def dump(self, content: Any) -> str:
        '''
        Dumps to a string the given objects
        '''
        raise NotImplementedError

    @abstractmethod
    def _read_content(self, type_code: int, block_data: bytes, class_desc: Optional[Any] = None) -> Any:
        '''
        Parses the next content. Use with care (use only in a transformer)
        '''
        raise NotImplementedError
