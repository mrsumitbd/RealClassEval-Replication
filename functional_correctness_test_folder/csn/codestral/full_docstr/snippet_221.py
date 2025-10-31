
import dataclasses


@dataclasses.dataclass
class Attachment:
    '''Dataclass representing an attachment.'''

    def to_dict(self) -> dict[str, str]:
        '''Convert to a dictionary for submitting to the REST API.'''
        return dataclasses.asdict(self)

    def multipart_form_element(self) -> tuple[str, bytes, str]:
        '''Convert to a tuple as required for multipart-form-data submission.'''
        return (self.name, self.content, self.content_type)
