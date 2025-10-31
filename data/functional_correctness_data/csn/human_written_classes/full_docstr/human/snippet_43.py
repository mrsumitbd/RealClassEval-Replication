from pynvim.msgpack_rpc.msgpack_stream import MsgpackStream

class Response:
    """Response to a msgpack-rpc request that came from Nvim.

    When Nvim sends a msgpack-rpc request, an instance of this class is
    created for remembering state required to send a response.
    """

    def __init__(self, msgpack_stream: MsgpackStream, request_id: int):
        """Initialize the Response instance."""
        self._msgpack_stream = msgpack_stream
        self._request_id = request_id

    def send(self, value, error=False):
        """Send the response.

        If `error` is True, it will be sent as an error.
        """
        if error:
            resp = [1, self._request_id, value, None]
        else:
            resp = [1, self._request_id, None, value]
        debug('sending response to request %d: %s', self._request_id, resp)
        self._msgpack_stream.send(resp)