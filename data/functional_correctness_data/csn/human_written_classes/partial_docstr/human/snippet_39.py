class Codec:
    """communication encoding for the watchman server"""
    transport = None

    def __init__(self, transport):
        self.transport = transport

    def receive(self):
        raise NotImplementedError()

    def send(self, *args):
        raise NotImplementedError()

    def setTimeout(self, value):
        self.transport.setTimeout(value)