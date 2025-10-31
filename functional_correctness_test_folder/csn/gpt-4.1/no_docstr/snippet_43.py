
class Response:

    def __init__(self, msgpack_stream, request_id: int):
        self.msgpack_stream = msgpack_stream
        self.request_id = request_id
        self.sent = False

    def send(self, value, error=False):
        if self.sent:
            raise RuntimeError("Response already sent")
        response = {
            "id": self.request_id,
            "result": None if error else value,
            "error": value if error else None
        }
        self.msgpack_stream.send(response)
        self.sent = True
