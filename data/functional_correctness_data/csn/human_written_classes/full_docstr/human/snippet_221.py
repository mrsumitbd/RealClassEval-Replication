import dataclasses
import base64

@dataclasses.dataclass
class Attachment:
    """Dataclass representing an attachment."""
    file_name: str
    file_type: str
    file_content: bytes

    def to_dict(self) -> dict[str, str]:
        """Convert to a dictionary for submitting to the REST API."""
        return {'FileName': self.file_name, 'FileType': self.file_type, 'FileContent': base64.b64encode(self.file_content).decode('utf-8')}

    def multipart_form_element(self) -> tuple[str, bytes, str]:
        """Convert to a tuple as required for multipart-form-data submission."""
        return (self.file_name, self.file_content, self.file_type)