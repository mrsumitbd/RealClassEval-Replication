
class NoOpTraceId:

    def __init__(self):
        self.id = None

    def to_id(self):
        return self.id
