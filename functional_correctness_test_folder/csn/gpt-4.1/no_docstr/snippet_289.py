
import zmq
import threading
import time


class ZMQDesignatedReceiversSender:

    def __init__(self, default_port, receivers):
        self.default_port = default_port
        self.receivers = receivers  # dict: {receiver_id: address}
        self.context = zmq.Context()
        self.sockets = {}  # {address: socket}
        self.lock = threading.Lock()
        self.closed = False

    def __call__(self, data):
        # data should be a dict: {receiver_id: message}
        results = {}
        for receiver_id, message in data.items():
            address = self.receivers.get(receiver_id)
            if address is None:
                results[receiver_id] = False
                continue
            try:
                self._send_to_address(address, message)
                results[receiver_id] = True
            except Exception:
                results[receiver_id] = False
        return results

    def _send_to_address(self, address, data, timeout=10):
        with self.lock:
            if address not in self.sockets:
                socket = self.context.socket(zmq.REQ)
                socket.setsockopt(zmq.LINGER, 0)
                socket.connect(address)
                self.sockets[address] = socket
            else:
                socket = self.sockets[address]
        poller = zmq.Poller()
        poller.register(socket, zmq.POLLIN)
        socket.send_pyobj(data)
        socks = dict(poller.poll(timeout * 1000))
        if socks.get(socket) == zmq.POLLIN:
            _ = socket.recv()
        else:
            raise TimeoutError(f"Timeout waiting for reply from {address}")

    def close(self):
        with self.lock:
            for socket in self.sockets.values():
                socket.close()
            self.sockets.clear()
            self.context.term()
            self.closed = True
