
import dataclasses


@dataclasses.dataclass
class Attachment:
    name: str
    content: bytes
    content_type: str

    def to_dict(self) -> dict[str, str]:
        return {
            'name': self.name,
            'content_type': self.content_type
        }

    def multipart_form_element(self) -> tuple[str, bytes, str]:
        return (self.name, self.content, self.content_type)
