
import msgpack


class Response:
    """
    A helper class to send a response over a MsgpackStream.
    """

    def __init__(self, msgpack_stream: "MsgpackStream", request_id: int):
        """
        Initialize the Response instance.

        Parameters
        ----------
        msgpack_stream : MsgpackStream
            The stream used to send the packed message.
        request_id : int
            The identifier of the request to which this response belongs.
        """
        self._stream = msgpack_stream
        self._request_id = request_id

    def send(self, value, error: bool = False):
        """
        Send the response.

        Parameters
        ----------
        value : Any
            The value to send back. If `error` is True, this will be sent as an
            error payload.
        error : bool, optional
            If True, the payload will be wrapped in an `error` field; otherwise
            it will be wrapped in a `result` field. Default is False.
        """
        payload = {
            "id": self._request_id,
            "result": value if not error else None,
            "error": value if error else None,
        }
        packed = msgpack.packb(payload, use_bin_type=True)
        self._stream.write(packed)
        # If the stream has a flush method, call it to ensure delivery.
        flush = getattr(self._stream, "flush", None)
        if callable(flush):
            flush()
