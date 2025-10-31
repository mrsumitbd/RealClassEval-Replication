
import uuid


class TraceId:

    def __init__(self):
        self.id = uuid.uuid4()

    def to_id(self):
        return str(self.id)
