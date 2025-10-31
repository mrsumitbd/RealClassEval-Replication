
from dataclasses import dataclass
import base64
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
        # Example validation logic
        if not hasattr(self, 'required_field') or not self.required_field:
            raise ValueError("Configuration is missing required_field")

    def to_dict(self) -> Dict:
        '''Convert to dictionary format for API request.
        Returns:
            Dict containing the configuration in API format
        Raises:
            ValueError: If configuration is invalid
        '''
        self.validate()
        return {field: getattr(self, field) for field in self.__dataclass_fields__.keys()}
