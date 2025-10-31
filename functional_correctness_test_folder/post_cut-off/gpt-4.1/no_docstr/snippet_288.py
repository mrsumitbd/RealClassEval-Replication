
from dataclasses import dataclass, field
from typing import Dict
import base64


@dataclass
class ParserExtensionConfig:
    # Example fields (can be adjusted as needed)
    enabled: bool = field(default=True)
    name: str = field(default="")
    version: str = field(default="1.0")

    @staticmethod
    def encode_base64(text: str) -> str:
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        if not isinstance(self.enabled, bool):
            raise ValueError("enabled must be a boolean")
        if not isinstance(self.name, str):
            raise ValueError("name must be a string")
        if not isinstance(self.version, str):
            raise ValueError("version must be a string")

    def to_dict(self) -> Dict:
        return {
            "enabled": self.enabled,
            "name": self.name,
            "version": self.version
        }
