
import dataclasses
from typing import Optional


@dataclasses.dataclass
class Attachment:
    filename: str
    content: bytes
    content_type: Optional[str] = None

    def to_dict(self) -> dict[str, str]:
        return {
            "filename": self.filename,
            "content_type": self.content_type or "application/octet-stream"
        }

    def multipart_form_element(self) -> tuple[str, bytes, str]:
        return (
            self.filename,
            self.content,
            self.content_type or "application/octet-stream"
        )
