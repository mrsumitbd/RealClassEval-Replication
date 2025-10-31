class NoOpTraceId:

    def __init__(self):
        self._id = None

    def to_id(self):
        return self._id
