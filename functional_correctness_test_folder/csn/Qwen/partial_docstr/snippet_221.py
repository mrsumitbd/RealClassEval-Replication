
import dataclasses
from typing import Any


@dataclasses.dataclass
class Attachment:
    '''Dataclass representing an attachment.'''
    filename: str
    content: bytes
    content_type: str

    def to_dict(self) -> dict[str, Any]:
        return {
            'filename': self.filename,
            'content_type': self.content_type
        }

    def multipart_form_element(self) -> tuple[str, bytes, str]:
        return (self.filename, self.content, self.content_type)
