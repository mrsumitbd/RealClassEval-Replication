
import base64
from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class ParserExtensionConfig:
    '''Parser extension configuration.'''

    @staticmethod
    def encode_base64(text: str) -> str:
        '''Encode a string to base64.
        Args:
            text: Raw string
        Returns:
            Base64 encoded string
        '''
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        encoded_bytes = base64.b64encode(text.encode('utf-8'))
        return encoded_bytes.decode('utf-8')

    def __post_init__(self) -> None:
        # No additional initialization required for the base class.
        pass

    def validate(self) -> None:
        '''Validate configuration.
        Raises:
            ValueError: If configuration is invalid
        '''
        # Base implementation does nothing; subclasses may override.
        pass

    def to_dict(self) -> Dict:
        '''Return a dictionary representation of the configuration.'''
        return asdict(self)
