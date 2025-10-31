
from __future__ import annotations

import base64
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class ParserExtensionConfig:
    """
    Parser extension configuration.

    Attributes
    ----------
    name : str
        Identifier for the parser extension.
    config : dict
        Configuration payload for the extension.
    enabled : bool, default True
        Flag indicating whether the extension is active.
    description : Optional[str], default None
        Human‑readable description of the extension.
    """

    name: str
    config: Dict[str, Any]
    enabled: bool = True
    description: Optional[str] = None

    @staticmethod
    def encode_base64(text: str) -> str:
        """
        Encode a string to base64.

        Parameters
        ----------
        text : str
            Raw string to encode.

        Returns
        -------
        str
            Base64 encoded string.
        """
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        return base64.b64encode(text.encode("utf-8")).decode("utf-8")

    def __post_init__(self) -> None:
        """Post initialization hook for field processing."""
        self.validate()

    def validate(self) -> None:
        """
        Validate configuration.

        Raises
        ------
        ValueError
            If configuration is invalid.
        """
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("`name` must be a non‑empty string")
        if not isinstance(self.config, dict):
            raise ValueError("`config` must be a dictionary")
        if not isinstance(self.enabled, bool):
            raise ValueError("`enabled` must be a boolean")
        if self.description is not None and not isinstance(self.description, str):
            raise ValueError("`description` must be a string if provided")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary format for API request.

        Returns
        -------
        dict
            Dictionary containing the configuration in API format.

        Raises
        ------
        ValueError
            If configuration is invalid.
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
