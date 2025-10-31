
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
        return base64.b64encode(text.encode()).decode()

    def __post_init__(self) -> None:
        '''Post initialization hook for field processing.'''
        self.validate()

    def validate(self) -> None:
        '''Validate configuration.
        Raises:
            ValueError: If configuration is invalid
        '''
        # Add validation logic here based on the actual fields in the dataclass
        # For demonstration purposes, assume there are no fields to validate
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
