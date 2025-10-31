
from __future__ import annotations

import base64
import re
from dataclasses import dataclass, field
from typing import Any, Dict, Mapping


@dataclass
class ParserExtensionConfig:
    """
    Configuration for a parser extension.

    Attributes
    ----------
    name : str
        The unique name of the extension.
    version : str
        Semantic version string (e.g. "1.0.0").
    config : Mapping[str, Any]
        Arbitrary configuration data for the extension.
    enabled : bool
        Whether the extension is enabled.
    """

    name: str
    version: str
    config: Mapping[str, Any] = field(default_factory=dict)
    enabled: bool = True

    @staticmethod
    def encode_base64(text: str) -> str:
        """
        Encode a string into base64.

        Parameters
        ----------
        text : str
            The text to encode.

        Returns
        -------
        str
            Base64 encoded representation of the input text.
        """
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        encoded_bytes = base64.b64encode(text.encode("utf-8"))
        return encoded_bytes.decode("utf-8")

    def __post_init__(self) -> None:
        """
        Validate the configuration after initialization.
        """
        self.validate()

    def validate(self) -> None:
        """
        Validate the configuration fields.

        Raises
        ------
        ValueError
            If any required field is missing or invalid.
        """
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("`name` must be a non-empty string")

        if not isinstance(self.version, str):
            raise ValueError("`version` must be a string")

        semver_pattern = r"^\d+\.\d+\.\d+$"
        if not re.match(semver_pattern, self.version):
            raise ValueError(
                f"`version` must follow semantic versioning (e.g. '1.0.0'), got: {self.version}"
            )

        if not isinstance(self.config, Mapping):
            raise ValueError("`config` must be a mapping (dict-like)")

        if not isinstance(self.enabled, bool):
            raise ValueError("`enabled` must be a boolean")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the configuration to a plain dictionary.

        Returns
        -------
        dict
            Dictionary representation of the configuration.
        """
        return {
            "name": self.name,
            "version": self.version,
            "config": dict(self.config),
            "enabled": self.enabled,
        }
