
import zmq
import threading
import time


class ZMQDesignatedReceiversSender:
    '''Sends message to multiple *receivers* on *port*.'''

    def __init__(self, default_port, receivers):
        '''Set up the sender.'''
        self.default_port = default_port
        self.receivers = receivers
        self.context = zmq.Context.instance()
        self.sockets = {}
        self.lock = threading.Lock()

        for addr in self.receivers:
            sock = self.context.socket(zmq.REQ)
            sock.setsockopt(zmq.SNDTIMEO, 10_000)  # 10 seconds default
            sock.setsockopt(zmq.RCVTIMEO, 10_000)
            sock.connect(f"tcp://{addr}:{self.default_port}")
            self.sockets[addr] = sock

    def __call__(self, data):
        '''Send data.'''
        for addr, sock in self.sockets.items():
            try:
                self._send_to_address(addr, data)
            except Exception:
                # If sending fails, we can log or ignore
                pass

    def _send_to_address(self, address, data, timeout=10):
        '''Send data to a specific address with a timeout.'''
        sock = self.sockets.get(address)
        if not sock:
            raise ValueError(f"No socket for address {address}")

        # Set timeouts
        sock.setsockopt(zmq.SNDTIMEO, timeout * 1000)
        sock.setsockopt(zmq.RCVTIMEO, timeout * 1000)

        # Send the data
        sock.send_pyobj(data)

        # Optionally wait for a reply (non-blocking)
        try:
            reply = sock.recv_pyobj(flags=zmq.NOBLOCK)
            return reply
        except zmq.Again:
            # No reply received within timeout
            return None

    def close(self):
        '''Close the sender.'''
        with self.lock:
            for sock in self.sockets.values():
                try:
                    sock.close()
                except Exception:
                    pass
            self.sockets.clear()
            try:
                self.context.term()
            except Exception:
                pass
