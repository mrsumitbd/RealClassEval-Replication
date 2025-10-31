
import dataclasses


@dataclasses.dataclass
class Attachment:
    '''Dataclass representing an attachment.'''
    name: str
    content: bytes
    content_type: str

    def to_dict(self) -> dict[str, str]:
        return {
            'name': self.name,
            'content_type': self.content_type,
            'content_length': str(len(self.content))
        }

    def multipart_form_element(self) -> tuple[str, bytes, str]:
        '''Convert to a tuple as required for multipart-form-data submission.'''
        return (self.name, self.content, self.content_type)
