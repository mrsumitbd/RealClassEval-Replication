
import msgpack


class MsgpackStream:
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(msgpack.packb(data))

    def flush(self):
        self.stream.flush()


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
            'id': self.request_id,
        }
        if error:
            response['error'] = value
        else:
            response['result'] = value
        self.msgpack_stream.write(response)
        self.msgpack_stream.flush()
