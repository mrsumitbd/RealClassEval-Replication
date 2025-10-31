
import uuid


class TraceId:

    def __init__(self):
        '''
        Generate a random trace id.
        '''
        self._id = uuid.uuid4().hex

    def to_id(self):
        '''
        Convert TraceId object to a string.
        '''
        return self._id
