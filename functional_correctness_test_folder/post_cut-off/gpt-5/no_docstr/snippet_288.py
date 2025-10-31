from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import base64


@dataclass
class ParserExtensionConfig:
    name: str
    version: str
    description: Optional[str] = None
    icon_text: Optional[str] = None
    icon_base64: Optional[str] = None
    settings: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True

    @staticmethod
    def encode_base64(text: str) -> str:
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        return base64.b64encode(text.encode("utf-8")).decode("ascii")

    def __post_init__(self) -> None:
        if self.icon_base64 is None and self.icon_text is not None:
            self.icon_base64 = self.encode_base64(self.icon_text)
        self.validate()

    def validate(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("name must be a non-empty string")
        if not isinstance(self.version, str) or not self.version.strip():
            raise ValueError("version must be a non-empty string")
        if self.description is not None and not isinstance(self.description, str):
            raise ValueError("description must be a string or None")
        if not isinstance(self.settings, dict):
            raise ValueError("settings must be a dictionary")
        if not isinstance(self.enabled, bool):
            raise ValueError("enabled must be a boolean")
        if self.icon_base64 is not None:
            if not isinstance(self.icon_base64, str) or not self.icon_base64.strip():
                raise ValueError(
                    "icon_base64 must be a non-empty string if provided")
            try:
                base64.b64decode(self.icon_base64, validate=True)
            except Exception as e:
                raise ValueError("icon_base64 is not valid base64") from e

    def to_dict(self) -> Dict:
        data: Dict[str, Any] = {
            "name": self.name,
            "version": self.version,
            "enabled": self.enabled,
            "settings": dict(self.settings),
        }
        if self.description is not None:
            data["description"] = self.description
        if self.icon_base64 is not None:
            data["icon_base64"] = self.icon_base64
        return data
