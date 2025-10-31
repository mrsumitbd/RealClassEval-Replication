
import msgpack


class Response:
    '''Response to a msgpack-rpc request that came from Nvim.
    When Nvim sends a msgpack-rpc request, an instance of this class is
    created for remembering state required to send a response.
    '''

    def __init__(self, msgpack_stream: 'MsgpackStream', request_id: int):
        '''Initialize the Response instance.'''
        self._stream = msgpack_stream
        self._request_id = request_id

    def send(self, value, error=False):
        '''Send the response.
        If `error` is True, it will be sent as an error.
        '''
        # According to msgpack-rpc spec:
        #   response = [msgid, [error, result]]
        #   error is None if no error, otherwise a string
        #   result is None if error
        if error:
            payload = [self._request_id, [value, None]]
        else:
            payload = [self._request_id, [None, value]]

        packed = msgpack.packb(payload, use_bin_type=True)
        # Write the packed data to the stream
        self._stream.write(packed)
        # Flush if the stream supports it
        flush = getattr(self._stream, 'flush', None)
        if callable(flush):
            flush()
