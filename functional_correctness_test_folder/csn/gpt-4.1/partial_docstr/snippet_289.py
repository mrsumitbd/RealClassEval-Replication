
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
            socket = self.context.socket(zmq.REQ)
            socket.connect(address)
            self.sockets[receiver] = socket

    def __call__(self, data):
        '''Send data.'''
        for receiver in self.receivers:
            address = f"tcp://{receiver}:{self.default_port}"
            self._send_to_address(address, data)

    def _send_to_address(self, address, data, timeout=10):
        # address is of the form tcp://host:port
        host_port = address.split("://")[1]
        host, port = host_port.split(":")
        receiver = host
        with self.lock:
            socket = self.sockets.get(receiver)
            if socket is None:
                socket = self.context.socket(zmq.REQ)
                socket.connect(address)
                self.sockets[receiver] = socket
            poller = zmq.Poller()
            poller.register(socket, zmq.POLLIN)
            try:
                socket.send_pyobj(data)
                socks = dict(poller.poll(timeout * 1000))
                if socks.get(socket) == zmq.POLLIN:
                    _ = socket.recv()
                else:
                    raise TimeoutError(
                        f"Timeout waiting for reply from {address}")
            finally:
                poller.unregister(socket)

    def close(self):
        '''Close the sender.'''
        with self.lock:
            for socket in self.sockets.values():
                socket.close()
            self.sockets.clear()
            self.context.term()
