
from __future__ import annotations

import base64
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class ParserExtensionConfig:
    """Parser extension configuration."""

    name: str
    config: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    description: Optional[str] = None

    @staticmethod
    def encode_base64(text: str) -> str:
        """Encode a string to base64.

        Args:
            text: Raw string

        Returns:
            Base64 encoded string
        """
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        return base64.b64encode(text.encode("utf-8")).decode("utf-8")

    def __post_init__(self) -> None:
        """Post initialization hook for field processing."""
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("name must be a non-empty string")
        if not isinstance(self.config, dict):
            raise TypeError("config must be a dictionary")
        if not isinstance(self.enabled, bool):
            raise TypeError("enabled must be a boolean")
        if self.description is not None and not isinstance(self.description, str):
            raise TypeError("description must be a string or None")

    def validate(self) -> None:
        """Validate configuration.

        Raises:
            ValueError: If configuration is invalid
        """
        if not self.name:
            raise ValueError("Configuration must have a non-empty name.")
        if not isinstance(self.config, dict):
            raise ValueError("Configuration 'config' must be a dictionary.")
        # Example rule: config must contain a 'type' key
        if "type" not in self.config:
            raise ValueError(
                "Configuration 'config' must contain a 'type' key.")
        # Example rule: type must be a string
        if not isinstance(self.config["type"], str):
            raise ValueError("Configuration 'config.type' must be a string.")
        # Additional custom validation can be added here

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format for API request.

        Returns:
            Dict containing the configuration in API format

        Raises:
            ValueError: If configuration is invalid
        """
        self.validate()
        result: Dict[str, Any] = {
            "name": self.name,
            "config": self.config,
            "enabled": self.enabled,
        }
        if self.description is not None:
            result["description"] = self.description
        return result
