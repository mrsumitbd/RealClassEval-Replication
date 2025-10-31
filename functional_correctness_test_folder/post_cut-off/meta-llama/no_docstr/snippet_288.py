
import base64
from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class ParserExtensionConfig:
    @staticmethod
    def encode_base64(text: str) -> str:
        text_bytes = text.encode('ascii')
        encoded_bytes = base64.b64encode(text_bytes)
        return encoded_bytes.decode('ascii')

    def __post_init__(self) -> None:
        pass

    def validate(self) -> None:
        pass

    def to_dict(self) -> Dict:
        return asdict(self)
