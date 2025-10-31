class Response:
    '''Response to a msgpack-rpc request that came from Nvim.
    When Nvim sends a msgpack-rpc request, an instance of this class is
    created for remembering state required to send a response.
    '''

    def __init__(self, msgpack_stream, request_id: int):
        '''Initialize the Response instance.'''
        self._msgpack_stream = msgpack_stream
        self._request_id = request_id
        self._sent = False

    def send(self, value, error=False):
        '''Send the response.
        If `error` is True, it will be sent as an error.
        '''
        if self._sent:
            return
        if error:
            msg = [1, self._request_id, value, None]
        else:
            msg = [1, self._request_id, None, value]
        self._msgpack_stream.send(msg)
        self._sent = True
