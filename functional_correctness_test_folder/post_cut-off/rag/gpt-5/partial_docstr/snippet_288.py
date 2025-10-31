from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import base64
import os


@dataclass
class ParserExtensionConfig:
    """Parser extension configuration."""
    name: Optional[str] = None
    language: Optional[str] = None
    source: Optional[str] = None
    source_b64: Optional[str] = None
    path: Optional[str] = None
    enabled: bool = True
    settings: Optional[Dict[str, Any]] = field(default_factory=dict)

    @staticmethod
    def encode_base64(text: str) -> str:
        """Encode a string to base64.
        Args:
            log: Raw string
        Returns:
            Base64 encoded string
        """
        if text is None:
            text = ""
        return base64.b64encode(text.encode("utf-8")).decode("ascii")

    def __post_init__(self) -> None:
        """Post initialization hook for field processing."""
        if self.settings is None:
            self.settings = {}

        if self.path and not self.source and not self.source_b64:
            if not os.path.exists(self.path):
                raise ValueError(f"File does not exist: {self.path}")
            if not os.path.isfile(self.path):
                raise ValueError(f"Path is not a file: {self.path}")
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self.source = f.read()
            except OSError as e:
                raise ValueError(f"Unable to read file: {self.path}") from e

        if self.source and not self.source_b64:
            self.source_b64 = self.encode_base64(self.source)

    def validate(self) -> None:
        """Validate configuration.
        Raises:
            ValueError: If configuration is invalid
        """
        # Ensure content is supplied
        if not (self.source_b64 or self.source or self.path):
            raise ValueError(
                "No source provided; set `source`, `source_b64`, or `path`.")

        # Validate provided base64
        if self.source_b64:
            try:
                base64.b64decode(self.source_b64.encode(
                    "ascii"), validate=True)
            except Exception as e:
                raise ValueError("`source_b64` is not valid Base64.") from e

        # Validate settings type
        if self.settings is not None and not isinstance(self.settings, dict):
            raise ValueError("`settings` must be a dictionary if provided.")

        # Optional: basic checks for language and name when provided
        if self.language is not None and not isinstance(self.language, str):
            raise ValueError("`language` must be a string when provided.")
        if self.name is not None and not isinstance(self.name, str):
            raise ValueError("`name` must be a string when provided.")

        # Ensure we have base64 content after post-init processing
        if not self.source_b64:
            # If source was empty or only whitespace, disallow
            if not self.source or not self.source.strip():
                raise ValueError("Source content is empty.")

    def to_dict(self) -> Dict:
        """Convert to dictionary format for API request.
        Returns:
            Dict containing the configuration in API format
        Raises:
            ValueError: If configuration is invalid
        """
        self.validate()
        payload: Dict[str, Any] = {
            "enabled": self.enabled,
            "content": self.source_b64,  # base64-encoded source
        }
        if self.name is not None:
            payload["name"] = self.name
        if self.language is not None:
            payload["language"] = self.language
        if self.settings:
            payload["settings"] = self.settings
        return payload
