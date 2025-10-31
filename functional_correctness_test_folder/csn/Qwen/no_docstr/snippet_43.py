
import msgpack


class MsgpackStream:
    def __init__(self):
        self.buffer = bytearray()

    def write(self, data):
        self.buffer.extend(data)

    def send(self):
        # Simulate sending the buffer over a network or saving it
        print("Sending:", self.buffer)
        self.buffer = bytearray()


class Response:

    def __init__(self, msgpack_stream: MsgpackStream, request_id: int):
        self.msgpack_stream = msgpack_stream
        self.request_id = request_id

    def send(self, value, error=False):
        response = {
            'request_id': self.request_id,
            'error': error,
            'value': value
        }
        packed = msgpack.packb(response)
        self.msgpack_stream.write(packed)
        self.msgpack_stream.send()
