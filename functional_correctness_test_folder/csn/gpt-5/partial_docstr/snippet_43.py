class Response:

    def __init__(self, msgpack_stream, request_id: int):
        self._stream = msgpack_stream
        self._id = request_id
        self._sent = False

    def send(self, value, error=False):
        if self._sent:
            raise RuntimeError("Response already sent")
        self._sent = True

        if error:
            err = value
            res = None
        else:
            err = None
            res = value

        msg = [1, self._id, err, res]

        send_method = getattr(self._stream, "send", None) or getattr(
            self._stream, "write", None) or getattr(self._stream, "send_msg", None)
        if send_method is None:
            raise AttributeError(
                "MsgpackStream does not have a send/write method")

        send_method(msg)
        return True
