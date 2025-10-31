class Response:
    def __init__(self, msgpack_stream, request_id: int):
        self._stream = msgpack_stream
        self._id = request_id
        self._sent = False

    def send(self, value, error: bool = False):
        if self._sent:
            return False

        if error:
            msg = [1, self._id, value, None]
        else:
            msg = [1, self._id, None, value]

        sent = False
        for method_name in ("send", "write", "write_msg", "push", "put"):
            method = getattr(self._stream, method_name, None)
            if callable(method):
                method(msg)
                sent = True
                break

        if not sent:
            pack = getattr(self._stream, "pack", None)
            if callable(pack):
                pack(msg)
                flush = getattr(self._stream, "flush", None)
                if callable(flush):
                    flush()
                sent = True

        self._sent = True
        return True
