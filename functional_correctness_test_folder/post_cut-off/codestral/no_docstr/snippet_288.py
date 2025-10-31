
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
        pass

    def to_dict(self) -> Dict:
        return self.__dict__
