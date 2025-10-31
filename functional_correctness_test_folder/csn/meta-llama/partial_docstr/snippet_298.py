
import zmq
import time

# Assuming _MAGICK is defined elsewhere in the codebase
_MAGICK = b'magick'


class Subscribe:

    def __init__(self, services='', topics=_MAGICK, addr_listener=False, addresses=None, timeout=10, translate=False, nameserver='localhost', message_filter=None):
        '''Initialize the class.'''
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.services = services
        self.topics = topics
        self.addr_listener = addr_listener
        self.addresses = addresses if addresses else []
        self.timeout = timeout
        self.translate = translate
        self.nameserver = nameserver
        self.message_filter = message_filter
        self.connected = False

    def __enter__(self):
        '''Start the subscriber when used as a context manager.'''
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        if not self.connected:
            if self.addr_listener:
                self.socket.bind('tcp://*:*')
                self.address = self.socket.getsockopt(
                    zmq.LAST_ENDPOINT).decode('utf-8')
            else:
                if not self.addresses:
                    # Assuming a nameserver is used to get the addresses
                    # For simplicity, this part is omitted
                    pass
                for address in self.addresses:
                    self.socket.connect(address)
            for topic in self.topics:
                self.socket.setsockopt(zmq.SUBSCRIBE, topic)
            self.connected = True

    def disconnect(self):
        if self.connected:
            self.socket.close()
            self.context.term()
            self.connected = False

    # Additional methods can be added here to handle messages, e.g.,
    def receive(self):
        if self.connected:
            try:
                return self.socket.recv_multipart(flags=zmq.NOBLOCK)
            except zmq.Again:
                return None
        else:
            raise Exception('Not connected')
