
import dataclasses
from typing import Optional


@dataclasses.dataclass
class Attachment:
    '''Dataclass representing an attachment.'''
    filename: str
    content: bytes
    content_type: Optional[str] = None

    def to_dict(self) -> dict[str, str]:
        '''Convert to a dictionary for submitting to the REST API.'''
        return {
            'filename': self.filename,
            'contentType': self.content_type or 'application/octet-stream'
        }

    def multipart_form_element(self) -> tuple[str, bytes, str]:
        '''Convert to a tuple as required for multipart-form-data submission.'''
        return (self.filename, self.content, self.content_type or 'application/octet-stream')
