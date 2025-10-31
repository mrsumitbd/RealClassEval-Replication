
import zmq
import socket as _socket


class ZMQDesignatedReceiversSender:
    '''Sends message to multiple *receivers* on *port*.'''

    def __init__(self, default_port, receivers):
        '''Set up the sender.'''
        self.default_port = default_port
        self.receivers = receivers
        self.context = zmq.Context()

    def __call__(self, data):
        '''Send data.'''
        for addr in self.receivers:
            self._send_to_address(addr, data)

    def _send_to_address(self, address, data, timeout=10):
        '''Send data to *address* and *port* without verification of response.'''
        # Resolve host:port
        if ':' in address:
            host, port_str = address.split(':', 1)
            try:
                port = int(port_str)
            except ValueError:
                port = self.default_port
        else:
            host = address
            port = self.default_port

        # Resolve hostname to IP
        try:
            ip = _socket.gethostbyname(host)
        except _socket.gaierror:
            # If resolution fails, skip this address
            return

        sock = self.context.socket(zmq.PUSH)
        sock.setsockopt(zmq.SNDTIMEO, timeout * 1000)  # timeout in ms
        try:
            sock.connect(f"tcp://{ip}:{port}")
            if isinstance(data, str):
                data = data.encode('utf-8')
            sock.send(data)
        except zmq.ZMQError:
            # ignore send errors (e.g., timeout)
            pass
        finally:
            sock.close()

    def close(self):
        '''Close the sender.'''
        self.context.term()
