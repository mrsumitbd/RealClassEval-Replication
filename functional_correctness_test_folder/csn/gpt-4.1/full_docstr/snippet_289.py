
import zmq
import threading


class ZMQDesignatedReceiversSender:
    '''Sends message to multiple *receivers* on *port*.'''

    def __init__(self, default_port, receivers):
        '''Set up the sender.'''
        self.default_port = default_port
        self.receivers = receivers
        self.context = zmq.Context()
        self.sockets = {}
        self.lock = threading.Lock()
        for receiver in receivers:
            address = f"tcp://{receiver}:{self.default_port}"
            socket = self.context.socket(zmq.PUSH)
            socket.connect(address)
            self.sockets[receiver] = socket

    def __call__(self, data):
        '''Send data.'''
        with self.lock:
            for receiver, socket in self.sockets.items():
                try:
                    socket.send_pyobj(data, zmq.NOBLOCK)
                except zmq.Again:
                    pass  # Non-blocking send, skip if not ready

    def _send_to_address(self, address, data, timeout=10):
        '''Send data to *address* and *port* without verification of response.'''
        socket = self.context.socket(zmq.PUSH)
        socket.setsockopt(zmq.SNDTIMEO, int(timeout * 1000))
        try:
            socket.connect(f"tcp://{address}:{self.default_port}")
            socket.send_pyobj(data)
        finally:
            socket.close()

    def close(self):
        '''Close the sender.'''
        with self.lock:
            for socket in self.sockets.values():
                socket.close()
            self.sockets.clear()
            self.context.term()
