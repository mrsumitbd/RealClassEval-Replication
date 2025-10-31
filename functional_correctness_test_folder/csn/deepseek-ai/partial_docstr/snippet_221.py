
import dataclasses
from typing import Optional


@dataclasses.dataclass
class Attachment:
    '''Dataclass representing an attachment.'''
    filename: str
    content_type: str
    data: bytes

    def to_dict(self) -> dict[str, str]:
        return {
            'filename': self.filename,
            'content_type': self.content_type,
        }

    def multipart_form_element(self) -> tuple[str, bytes, str]:
        '''Convert to a tuple as required for multipart-form-data submission.'''
        return (self.filename, self.data, self.content_type)
