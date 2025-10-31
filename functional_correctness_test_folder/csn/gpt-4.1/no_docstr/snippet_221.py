
import dataclasses


@dataclasses.dataclass
class Attachment:
    filename: str
    content: bytes
    mimetype: str

    def to_dict(self) -> dict[str, str]:
        return {
            "filename": self.filename,
            "mimetype": self.mimetype
        }

    def multipart_form_element(self) -> tuple[str, bytes, str]:
        return (self.filename, self.content, self.mimetype)
