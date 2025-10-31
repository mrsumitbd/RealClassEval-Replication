
from __future__ import annotations

import base64
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional


@dataclass
class ParserExtensionConfig:
    """
    Parser extension configuration.

    This class is intentionally lightweight and flexible.  It can be
    instantiated with any keyword arguments – they will be stored as
    attributes on the instance.  The helper methods below operate on
    whatever data is present.
    """

    # No explicit fields – the dataclass will accept any keyword
    # arguments and store them as attributes.

    @staticmethod
    def encode_base64(text: str) -> str:
        """
        Encode a string to base64.

        Args:
            text: Raw string

        Returns:
            Base64 encoded string
        """
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        return base64.b64encode(text.encode("utf-8")).decode("utf-8")

    def __post_init__(self) -> None:
        """
        Post initialization hook for field processing.
        """
        # No mandatory fields – subclasses or callers can add logic here.
        pass

    def validate(self) -> None:
        """
        Validate configuration.

        Raises:
            ValueError: If configuration is invalid
        """
        # Basic validation: ensure that any attribute named 'name' is a non-empty string
        name = getattr(self, "name", None)
        if name is not None and not isinstance(name, str):
            raise ValueError("`name` must be a string if provided")
        if name is not None and not name.strip():
            raise ValueError("`name` cannot be empty")

        # Ensure that any attribute named 'config' is a dict if present
        cfg = getattr(self, "config", None)
        if cfg is not None and not isinstance(cfg, dict):
            raise ValueError("`config` must be a dict if provided")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary format for API request.

        Returns:
            Dict containing the configuration in API format

        Raises:
            ValueError: If configuration is invalid
        """
        # Validate before conversion
        self.validate()

        # Use asdict to handle nested dataclasses, but filter out private attributes
        result = asdict(self)
        # Remove any keys that start with an underscore (private/internal)
        return {k: v for k, v in result.items() if not k.startswith("_")}
