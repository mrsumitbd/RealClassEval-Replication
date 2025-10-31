
from dataclasses import dataclass, field
from typing import Dict
import base64


@dataclass
class ParserExtensionConfig:
    '''Parser extension configuration.'''
    # Example fields (can be adjusted as needed)
    enabled: bool = field(default=True)
    name: str = field(default="")
    options: Dict = field(default_factory=dict)

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
        if not isinstance(self.options, dict):
            self.options = dict(self.options)
        self.validate()

    def validate(self) -> None:
        '''Validate configuration.
        Raises:
            ValueError: If configuration is invalid
        '''
        if not isinstance(self.enabled, bool):
            raise ValueError("enabled must be a boolean")
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("name must be a non-empty string")
        if not isinstance(self.options, dict):
            raise ValueError("options must be a dictionary")

    def to_dict(self) -> Dict:
        '''Convert to dictionary format for API request.
        Returns:
            Dict containing the configuration in API format
        Raises:
            ValueError: If configuration is invalid
        '''
        self.validate()
        return {
            "enabled": self.enabled,
            "name": self.name,
            "options": self.options
        }
