from __future__ import annotations

import base64
import json
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class ParserExtensionConfig:
    '''Parser extension configuration.'''

    name: str = ""
    version: Optional[str] = None
    enabled: bool = True
    description: Optional[str] = None
    options: Dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def encode_base64(text: str) -> str:
        '''Encode a string to base64.
        Args:
            log: Raw string
        Returns:
            Base64 encoded string
        '''
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        return base64.b64encode(text.encode("utf-8")).decode("ascii")

    def __post_init__(self) -> None:
        if not isinstance(self.options, dict):
            raise TypeError("options must be a dict")
        # Normalize option keys to strings
        self.options = {str(k): v for k, v in self.options.items()}
        if isinstance(self.name, str):
            self.name = self.name.strip()
        if isinstance(self.version, str):
            self.version = self.version.strip() or None
        if isinstance(self.description, str):
            self.description = self.description.strip() or None
        self.validate()

    def validate(self) -> None:
        '''Validate configuration.
        Raises:
            ValueError: If configuration is invalid
        '''
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("name must be a non-empty string")
        if len(self.name) > 256:
            raise ValueError("name must be at most 256 characters")
        if self.version is not None and (not isinstance(self.version, str) or not self.version):
            raise ValueError(
                "version must be a non-empty string when provided")
        if not isinstance(self.enabled, bool):
            raise ValueError("enabled must be a boolean")
        if self.description is not None and not isinstance(self.description, str):
            raise ValueError("description must be a string when provided")
        if not isinstance(self.options, dict):
            raise ValueError("options must be a dict")
        for k in self.options.keys():
            if not isinstance(k, str) or not k:
                raise ValueError("all option keys must be non-empty strings")
        # Ensure options is JSON-serializable
        try:
            json.dumps(self.options)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"options must be JSON-serializable: {exc}") from exc

    def to_dict(self) -> Dict:
        data: Dict[str, Any] = {
            "name": self.name,
            "enabled": self.enabled,
            "options": self.options,
        }
        if self.version is not None:
            data["version"] = self.version
        if self.description is not None:
            data["description"] = self.description
        return data
