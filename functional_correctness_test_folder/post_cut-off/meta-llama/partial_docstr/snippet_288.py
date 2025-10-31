
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
        self.validate()

    def validate(self) -> None:
        '''Validate configuration.
        Raises:
            ValueError: If configuration is invalid
        '''
        # Add validation logic here as per your requirements
        # For demonstration, let's assume we have a field 'required_field'
        if not hasattr(self, 'required_field') or not self.required_field:
            raise ValueError("Configuration is invalid")

    def to_dict(self) -> Dict:
        return asdict(self)
