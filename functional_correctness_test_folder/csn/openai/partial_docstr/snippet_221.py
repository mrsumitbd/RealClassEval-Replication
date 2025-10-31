
import dataclasses
from dataclasses import dataclass, field
from typing import Tuple, Dict


@dataclass
class Attachment:
    """Dataclass representing an attachment."""

    filename: str
    content_type: str
    data: bytes = field(repr=False)

    def to_dict(self) -> Dict[str, str]:
        """Return a dictionary representation of the attachment."""
        return {
            "filename": self.filename,
            "content_type": self.content_type,
        }

    def multipart_form_element(self) -> Tuple[str, bytes, str]:
        """
        Convert to a tuple as required for multipart-form-data submission.

        Returns:
            A tuple of (filename, data, content_type).
        """
        return self.filename, self.data, self.content_type
