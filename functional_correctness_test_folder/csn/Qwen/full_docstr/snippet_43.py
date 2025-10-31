
class Response:
    '''Response to a msgpack-rpc request that came from Nvim.
    When Nvim sends a msgpack-rpc request, an instance of this class is
    created for remembering state required to send a response.
    '''

    def __init__(self, msgpack_stream: MsgpackStream, request_id: int):
        '''Initialize the Response instance.'''
        self.msgpack_stream = msgpack_stream
        self.request_id = request_id

    def send(self, value, error=False):
        '''Send the response.
        If `error` is True, it will be sent as an error.
        '''
        if error:
            self.msgpack_stream.send_response(self.request_id, None, value)
        else:
            self.msgpack_stream.send_response(self.request_id, value, None)
