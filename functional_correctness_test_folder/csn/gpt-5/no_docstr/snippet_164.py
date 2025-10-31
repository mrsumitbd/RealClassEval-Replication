import uuid
from datetime import datetime


class patch_obj:

    def __init__(self):
        self.id = uuid.uuid4().hex
        self.created_at = datetime.utcnow()
        self.metadata = {}

    def __str__(self):
        return f"patch_obj(id={self.id}, created_at={self.created_at.isoformat()}Z, metadata={self.metadata})"
