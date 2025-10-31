
import uuid


class TraceId:

    def __init__(self):
        self.id = uuid.uuid4().hex

    def to_id(self):
        return self.id


# Example usage:
if __name__ == "__main__":
    trace_id = TraceId()
    print(trace_id.to_id())
