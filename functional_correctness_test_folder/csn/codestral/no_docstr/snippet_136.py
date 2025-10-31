
import uuid


class TraceId:

    def __init__(self):
        self._id = str(uuid.uuid4())

    def to_id(self):
        return self._id
