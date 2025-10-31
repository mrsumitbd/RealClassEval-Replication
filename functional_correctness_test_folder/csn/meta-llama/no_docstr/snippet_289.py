
import zmq
import pickle


class ZMQDesignatedReceiversSender:

    def __init__(self, default_port, receivers):
        self.context = zmq.Context()
        self.default_port = default_port
        self.receivers = receivers
        self.sockets = {}
        for receiver in receivers:
            self.sockets[receiver] = self.context.socket(zmq.PUSH)
            self.sockets[receiver].connect(f"tcp://{receiver}:{default_port}")

    def __call__(self, data):
        for receiver in self.receivers:
            self._send_to_address(receiver, data)

    def _send_to_address(self, address, data, timeout=10):
        if address not in self.sockets:
            raise ValueError(f"Unknown receiver: {address}")
        try:
            self.sockets[address].send(pickle.dumps(data), zmq.NOBLOCK)
        except zmq.Again:
            # Handle timeout or retry logic if needed
            pass

    def close(self):
        for socket in self.sockets.values():
            socket.close()
        self.context.term()
