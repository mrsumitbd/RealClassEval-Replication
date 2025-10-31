
from dataclasses import dataclass
import base64
from typing import Dict


@dataclass
class ParserExtensionConfig:

    @staticmethod
    def encode_base64(text: str) -> str:
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        # Example validation: ensure all attributes are of expected types
        for field in self.__dataclass_fields__.values():
            value = getattr(self, field.name)
            if not isinstance(value, field.type):
                raise ValueError(
                    f"Field {field.name} is not of type {field.type}")

    def to_dict(self) -> Dict:
        return {field.name: getattr(self, field.name) for field in self.__dataclass_fields__.values()}
