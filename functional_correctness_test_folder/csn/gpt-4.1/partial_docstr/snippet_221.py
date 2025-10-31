
import dataclasses


@dataclasses.dataclass
class Attachment:
    '''Dataclass representing an attachment.'''
    filename: str
    content: bytes
    mimetype: str

    def to_dict(self) -> dict[str, str]:
        return {
            "filename": self.filename,
            "mimetype": self.mimetype
        }

    def multipart_form_element(self) -> tuple[str, bytes, str]:
        '''Convert to a tuple as required for multipart-form-data submission.'''
        return (self.filename, self.content, self.mimetype)
