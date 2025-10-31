
import dataclasses
import mimetypes
from pathlib import Path


@dataclasses.dataclass
class Attachment:
    filename: str
    data: bytes

    def to_dict(self) -> dict[str, str]:
        return {"filename": self.filename}

    def multipart_form_element(self) -> tuple[str, bytes, str]:
        mime_type, _ = mimetypes.guess_type(self.filename)
        return (self.filename, self.data, mime_type or "application/octet-stream")
