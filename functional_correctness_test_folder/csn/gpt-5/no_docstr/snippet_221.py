from __future__ import annotations

import base64
import dataclasses
from typing import Union


@dataclasses.dataclass
class Attachment:
    filename: str
    data: bytes
    content_type: str = "application/octet-stream"

    def __post_init__(self) -> None:
        if isinstance(self.data, str):
            self.data = self.data.encode("utf-8")
        elif not isinstance(self.data, (bytes, bytearray, memoryview)):
            raise TypeError(
                "data must be bytes, bytearray, memoryview, or str")
        if isinstance(self.data, (bytearray, memoryview)):
            self.data = bytes(self.data)

    def to_dict(self) -> dict[str, str]:
        return {
            "filename": self.filename,
            "content": base64.b64encode(self.data).decode("ascii"),
            "content_type": self.content_type,
        }

    def multipart_form_element(self) -> tuple[str, bytes, str]:
        return (self.filename, self.data, self.content_type)
