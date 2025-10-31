
import base64
import dataclasses
from typing import Tuple, Dict


@dataclasses.dataclass
class Attachment:
    """Dataclass representing an attachment."""

    name: str
    content_type: str
    data: bytes

    def to_dict(self) -> Dict[str, str]:
        """Convert to a dictionary for submitting to the REST API."""
        return {
            "name": self.name,
            "content_type": self.content_type,
            "data": base64.b64encode(self.data).decode("utf-8"),
        }

    def multipart_form_element(self) -> Tuple[str, bytes, str]:
        """Convert to a tuple as required for multipart-form-data submission."""
        return (self.name, self.data, self.content_type)
