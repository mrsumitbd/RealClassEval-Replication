
import uuid


class TraceId:

    def __init__(self):
        self._id = uuid.uuid4().hex

    def to_id(self):
        return self._id
