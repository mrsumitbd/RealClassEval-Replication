
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
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
        encoded_bytes = base64.b64encode(text.encode('utf-8'))
        return encoded_bytes.decode('utf-8')

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        '''Validate configuration.
        Raises:
            ValueError: If configuration is invalid
        '''
        # No fields to validate in base class, but method exists for extension.
        pass

    def to_dict(self) -> Dict:
        return {}
