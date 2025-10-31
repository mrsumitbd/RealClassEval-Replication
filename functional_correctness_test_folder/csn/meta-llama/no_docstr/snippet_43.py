
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
        self.msgpack_stream = msgpack_stream
        self.request_id = request_id

    def send(self, value, error=False):
        response = {
            'id': self.request_id,
            'error': error,
            'result': value if not error else str(value)
        }
        self.msgpack_stream.write(response)
        self.msgpack_stream.flush()
