
from dataclasses import dataclass, field
from typing import Dict
import base64


@dataclass
class ParserExtensionConfig:
    '''Parser extension configuration.'''
    extension_name: str = field(default_factory=str)
    extension_version: str = field(default_factory=str)
    extension_enabled: bool = field(default=True)

    @staticmethod
    def encode_base64(text: str) -> str:
        '''Encode a string to base64.
        Args:
            text: Raw string
        Returns:
            Base64 encoded string
        '''
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')

    def __post_init__(self) -> None:
        '''Post initialization hook for field processing.'''
        self.validate()

    def validate(self) -> None:
        '''Validate configuration.
        Raises:
            ValueError: If configuration is invalid
        '''
        if not self.extension_name:
            raise ValueError("extension_name must be provided")
        if not self.extension_version:
            raise ValueError("extension_version must be provided")

    def to_dict(self) -> Dict:
        '''Convert to dictionary format for API request.
        Returns:
            Dict containing the configuration in API format
        Raises:
            ValueError: If configuration is invalid
        '''
        self.validate()
        return {
            'extension_name': self.extension_name,
            'extension_version': self.extension_version,
            'extension_enabled': self.extension_enabled
        }
