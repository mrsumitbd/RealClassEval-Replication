
from __future__ import annotations

import base64
import json
from dataclasses import dataclass, fields, is_dataclass
from typing import Any, Dict


@dataclass
class ParserExtensionConfig:
    """Parser extension configuration."""

    @staticmethod
    def encode_base64(text: str) -> str:
        """Encode a string to base64.

        Args:
            text: Raw string

        Returns:
            Base64 encoded string
        """
        if not isinstance(text, str):
            raise TypeError("encode_base64 expects a string")
        return base64.b64encode(text.encode("utf-8")).decode("utf-8")

    def __post_init__(self) -> None:
        """Post initialization hook for field processing."""
        # Perform validation after dataclass initialization
        self.validate()

    def validate(self) -> None:
        """Validate configuration.

        Raises:
            ValueError: If configuration is invalid
        """
        # Basic validation: ensure that all fields that are not optional
        # (i.e., have no default value) are set.
        for f in fields(self):
            # Skip fields with a default value or default_factory
            if f.default is not dataclass._MISSING_TYPE and f.default is not None:
                continue
            if f.default_factory is not dataclass._MISSING_TYPE:
                continue
            # If the field is None, raise an error
            if getattr(self, f.name) is None:
                raise ValueError(f"Field '{f.name}' is required but not set")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format for API request.

        Returns:
            Dict containing the configuration in API format

        Raises:
            ValueError: If configuration is invalid
        """
        # Validate before conversion
        self.validate()

        def _to_dict(obj: Any) -> Any:
            if is_dataclass(obj):
                return {f.name: _to_dict(getattr(obj, f.name)) for f in fields(obj)}
            if isinstance(obj, list):
                return [_to_dict(v) for v in obj]
            return obj

        return _to_dict(self)
