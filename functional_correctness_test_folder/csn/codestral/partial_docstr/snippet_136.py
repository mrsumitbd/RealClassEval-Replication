
import uuid


class TraceId:

    def __init__(self):
        '''
        Generate a random trace id.
        '''
        self.trace_id = str(uuid.uuid4())

    def to_id(self):
        '''
        Convert TraceId object to a string.
        '''
        return self.trace_id
