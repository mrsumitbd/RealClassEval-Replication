class NoOpTraceId:

    def __init__(self):
        self._id = ""

    def to_id(self):
        '''
        Convert TraceId object to a string.
        '''
        return self._id
