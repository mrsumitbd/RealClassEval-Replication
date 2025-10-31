
import msgpack


class MsgpackStream:
    def __init__(self, stream):
        self.stream = stream

    def send(self, data):
        self.stream.write(msgpack.packb(data))


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
        response = [1, self.request_id,
                    None if not error else value, value if not error else None]
        self.msgpack_stream.send(response)


# Example usage
if __name__ == "__main__":
    import io

    # Create a stream
    stream = io.BytesIO()
    msgpack_stream = MsgpackStream(stream)

    # Create a Response instance
    response = Response(msgpack_stream, 1)

    # Send a response
    response.send("Hello, World!")

    # Send an error response
    response.send("Something went wrong", error=True)

    # Print the sent data
    stream.seek(0)
    print(msgpack.unpackb(stream.read()))
    stream.seek(0)
    print(msgpack.unpackb(stream.read()))
