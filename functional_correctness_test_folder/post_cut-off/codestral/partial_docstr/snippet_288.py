
from dataclasses import dataclass
from typing import Dict
import base64


@dataclass
class ParserExtensionConfig:
    '''Parser extension configuration.'''

    @staticmethod
    def encode_base64(text: str) -> str:
        '''Encode a string to base64.
        Args:
            log: Raw string
        Returns:
            Base64 encoded string
        '''
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')

    def __post_init__(self) -> None:
        pass

    def validate(self) -> None:
        '''Validate configuration.
        Raises:
            ValueError: If configuration is invalid
        '''
        pass

    def to_dict(self) -> Dict:
        return self.__dict__
