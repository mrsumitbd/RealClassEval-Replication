from dataclasses import dataclass, field, asdict
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
        '''Post initialization hook for field processing.'''
        # No default post-init logic, but could be extended for field processing
        pass

    def validate(self) -> None:
        '''Validate configuration.
        Raises:
            ValueError: If configuration is invalid
        '''
        # Example: If there are required fields, check here.
        # Since no fields are defined, nothing to validate.
        # Extend this method if fields are added.
        pass

    def to_dict(self) -> Dict:
        '''Convert to dictionary format for API request.
        Returns:
            Dict containing the configuration in API format
        Raises:
            ValueError: If configuration is invalid
        '''
        self.validate()
        return asdict(self)
