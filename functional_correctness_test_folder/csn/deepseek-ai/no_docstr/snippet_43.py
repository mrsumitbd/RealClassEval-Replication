
class Response:

    def __init__(self, msgpack_stream: MsgpackStream, request_id: int):
        self.msgpack_stream = msgpack_stream
        self.request_id = request_id

    def send(self, value, error=False):
        response = {
            'id': self.request_id,
            'result': None if error else value,
            'error': value if error else None
        }
        self.msgpack_stream.send(response)
