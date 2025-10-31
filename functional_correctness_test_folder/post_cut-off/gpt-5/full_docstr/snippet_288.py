from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import base64


@dataclass
class ParserExtensionConfig:
    '''Parser extension configuration.'''
    name: str = ""
    description: Optional[str] = None
    enabled: bool = True
    settings: Dict[str, Any] = field(default_factory=dict)
    code: Optional[str] = None
    files: Dict[str, str] = field(default_factory=dict)

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
        '''Post initialization hook for field processing.'''
        if self.name is None:
            self.name = ""
        if not isinstance(self.name, str):
            raise TypeError("name must be a string")
        self.name = self.name.strip()

        if self.description is not None:
            if not isinstance(self.description, str):
                raise TypeError("description must be a string or None")
            self.description = self.description.strip()

        if not isinstance(self.enabled, bool):
            raise TypeError("enabled must be a bool")

        if not isinstance(self.settings, dict):
            raise TypeError("settings must be a dict")

        if self.code is not None and not isinstance(self.code, str):
            raise TypeError("code must be a string or None")

        if not isinstance(self.files, dict):
            raise TypeError("files must be a dict")
        # Ensure keys and values in files are strings
        normalized_files: Dict[str, str] = {}
        for k, v in self.files.items():
            if not isinstance(k, str) or not isinstance(v, str):
                raise TypeError("files keys and values must be strings")
            key = k.strip()
            if not key:
                raise ValueError("files cannot contain empty file names")
            normalized_files[key] = v
        self.files = normalized_files

    def validate(self) -> None:
        '''Validate configuration.
        Raises:
            ValueError: If configuration is invalid
        '''
        if not self.name:
            raise ValueError("name is required")
        if any(k is None for k in self.settings.keys()):
            raise ValueError("settings cannot contain None keys")
        if self.code is not None and self.code.strip() == "":
            raise ValueError("code cannot be an empty string when provided")
        for filename, content in self.files.items():
            if content is None or content == "":
                raise ValueError(f"file '{filename}' has empty content")

    def to_dict(self) -> Dict:
        '''Convert to dictionary format for API request.
        Returns:
            Dict containing the configuration in API format
        Raises:
            ValueError: If configuration is invalid
        '''
        self.validate()

        out: Dict[str, Any] = {
            "name": self.name,
            "enabled": self.enabled,
            "settings": self.settings.copy(),
        }
        if self.description:
            out["description"] = self.description

        if self.code is not None:
            out["code_b64"] = self.encode_base64(self.code)

        if self.files:
            out["files_b64"] = {fname: self.encode_base64(
                content) for fname, content in self.files.items()}

        return out
