
class Response:

    def __init__(self, msgpack_stream: MsgpackStream, request_id: int):
        self.msgpack_stream = msgpack_stream
        self.request_id = request_id

    def send(self, value, error=False):
        response = {
            'request_id': self.request_id,
            'value': value,
            'error': error
        }
        self.msgpack_stream.send(response)
