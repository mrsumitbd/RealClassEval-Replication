
from dataclasses import dataclass
import base64
from typing import Dict


@dataclass
class ParserExtensionConfig:
    """Parser extension configuration."""
    @staticmethod
    def encode_base64(text: str) -> str:
        """Encode a string to base64.
        Args:
            log: Raw string
        Returns:
            Base64 encoded string
        """
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')

    def __post_init__(self) -> None:
        """Post initialization hook for field processing."""
        self.validate()

    def validate(self) -> None:
        """Validate configuration.
        Raises:
            ValueError: If configuration is invalid
        """
        pass  # No validation needed in base class

    def to_dict(self) -> Dict:
        """Convert to dictionary format for API request.
        Returns:
            Dict containing the configuration in API format
        Raises:
            ValueError: If configuration is invalid
        """
        self.validate()
        return {}
