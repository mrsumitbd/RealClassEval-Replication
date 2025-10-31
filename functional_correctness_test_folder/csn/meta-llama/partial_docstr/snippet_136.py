
import uuid


class TraceId:

    def __init__(self):
        '''
        Generate a random trace id.
        '''
        self.trace_id = uuid.uuid4().hex

    def to_id(self):
        '''
        Convert TraceId object to a string.
        '''
        return self.trace_id


# Example usage:
if __name__ == "__main__":
    trace = TraceId()
    print(trace.to_id())
