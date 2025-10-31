
import zmq
import json
from threading import Lock


class ZMQDesignatedReceiversSender:
    '''Sends message to multiple *receivers* on *port*.'''

    def __init__(self, default_port, receivers):
        '''Set up the sender.'''
        self.default_port = default_port
        self.receivers = receivers
        self.context = zmq.Context()
        self.sockets = {}
        self.lock = Lock()

    def __call__(self, data):
        '''Send data.'''
        for receiver in self.receivers:
            self._send_to_address(receiver, data)

    def _send_to_address(self, address, data, timeout=10):
        with self.lock:
            if address not in self.sockets:
                socket = self.context.socket(zmq.PUSH)
                socket.setsockopt(zmq.LINGER, 0)
                socket.connect(f"tcp://{address}:{self.default_port}")
                self.sockets[address] = socket
            try:
                self.sockets[address].send_json(data, zmq.NOBLOCK)
            except zmq.Again:
                pass

    def close(self):
        '''Close the sender.'''
        with self.lock:
            for socket in self.sockets.values():
                socket.close()
            self.context.term()
