
import msgpack


class Response:
    def __init__(self, msgpack_stream: "MsgpackStream", request_id: int):
        self._stream = msgpack_stream
        self._request_id = request_id

    def send(self, value, error: bool = False):
        """
        Send a response back over the msgpack stream.

        Parameters
        ----------
        value : Any
            The payload to send. If `error` is True, this will be sent as an error.
        error : bool, optional
            If True, the payload is treated as an error message.
        """
        if error:
            payload = {"id": self._request_id, "error": value}
        else:
            payload = {"id": self._request_id, "result": value}

        packed = msgpack.packb(payload, use_bin_type=True)
        # Assume the stream has a write method that accepts bytes
        self._stream.write(packed)
