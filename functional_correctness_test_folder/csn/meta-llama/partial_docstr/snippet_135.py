
class NoOpTraceId:

    def __init__(self):
        pass

    def to_id(self):
        '''
        Convert TraceId object to a string.
        '''
        return 'noop'
