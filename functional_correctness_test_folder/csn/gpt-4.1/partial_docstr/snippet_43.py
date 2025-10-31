
class Response:

    def __init__(self, msgpack_stream, request_id: int):
        '''Initialize the Response instance.'''
        self.msgpack_stream = msgpack_stream
        self.request_id = request_id

    def send(self, value, error=False):
        '''Send the response.
        If `error` is True, it will be sent as an error.
        '''
        if error:
            response = [1, self.request_id, value, None]
        else:
            response = [1, self.request_id, None, value]
        self.msgpack_stream.send(response)
