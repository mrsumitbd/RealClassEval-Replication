
import dataclasses
from typing import Optional


@dataclasses.dataclass
class Attachment:
    '''Dataclass representing an attachment.'''
    filename: str
    content_type: str
    content: bytes
    id: Optional[str] = None

    def to_dict(self) -> dict[str, str]:
        '''Convert to a dictionary for submitting to the REST API.'''
        return {
            'filename': self.filename,
            'content_type': self.content_type,
            'id': self.id if self.id is not None else ''
        }

    def multipart_form_element(self) -> tuple[str, bytes, str]:
        '''Convert to a tuple as required for multipart-form-data submission.'''
        return (self.filename, self.content, self.content_type)
