import dataclasses
import base64
from typing import Union


@dataclasses.dataclass
class Attachment:
    '''Dataclass representing an attachment.'''
    filename: str
    content: Union[bytes, str]
    content_type: str = 'application/octet-stream'

    def __post_init__(self) -> None:
        if isinstance(self.content, str):
            self.content = self.content.encode('utf-8')

    def to_dict(self) -> dict[str, str]:
        '''Convert to a dictionary for submitting to the REST API.'''
        return {
            'filename': self.filename,
            'content': base64.b64encode(self.content).decode('ascii'),
            'content_type': self.content_type,
        }

    def multipart_form_element(self) -> tuple[str, bytes, str]:
        '''Convert to a tuple as required for multipart-form-data submission.'''
        return (self.filename, self.content, self.content_type)
