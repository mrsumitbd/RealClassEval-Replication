
class Response:

    def __init__(self, msgpack_stream: MsgpackStream, request_id: int):
        '''Initialize the Response instance.'''
        self.msgpack_stream = msgpack_stream
        self.request_id = request_id

    def send(self, value, error=False):
        '''Send the response.
        If `error` is True, it will be sent as an error.
        '''
        response = {
            'request_id': self.request_id,
            'error' if error else 'result': value
        }
        self.msgpack_stream.send(response)
