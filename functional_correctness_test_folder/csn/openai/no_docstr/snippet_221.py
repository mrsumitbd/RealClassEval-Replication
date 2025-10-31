
import dataclasses
from typing import Tuple, Dict


@dataclasses.dataclass
class Attachment:
    filename: str
    content: bytes
    content_type: str = "application/octet-stream"

    def to_dict(self) -> Dict[str, str]:
        return {
            "filename": self.filename,
            "content_type": self.content_type,
        }

    def multipart_form_element(self) -> Tuple[str, bytes, str]:
        return (self.filename, self.content, self.content_type)
