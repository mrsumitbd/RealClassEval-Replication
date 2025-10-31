import dataclasses
import base64


@dataclasses.dataclass
class Attachment:
    '''Dataclass representing an attachment.'''
    filename: str
    content: bytes
    content_type: str = "application/octet-stream"

    def __post_init__(self):
        if isinstance(self.content, str):
            self.content = self.content.encode("utf-8")
        if not isinstance(self.content, (bytes, bytearray)):
            raise TypeError("content must be bytes, bytearray, or str")
        if isinstance(self.content, bytearray):
            self.content = bytes(self.content)
        if not isinstance(self.filename, str) or not self.filename:
            raise ValueError("filename must be a non-empty string")
        if not isinstance(self.content_type, str) or not self.content_type:
            raise ValueError("content_type must be a non-empty string")

    def to_dict(self) -> dict[str, str]:
        return {
            "filename": self.filename,
            "content": base64.b64encode(self.content).decode("ascii"),
            "content_type": self.content_type,
        }

    def multipart_form_element(self) -> tuple[str, bytes, str]:
        '''Convert to a tuple as required for multipart-form-data submission.'''
        return (self.filename, self.content, self.content_type)
