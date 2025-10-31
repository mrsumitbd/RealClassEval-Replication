import secrets


class TraceId:

    def __init__(self):
        '''
        Generate a random trace id.
        '''
        self._id = secrets.token_hex(16)

    def to_id(self):
        '''
        Convert TraceId object to a string.
        '''
        return self._id
