import zmq
import pickle


class ZMQDesignatedReceiversSender:
    '''Sends message to multiple receivers on port.'''

    def __init__(self, default_port, receivers):
        '''Set up the sender.'''
        self._ctx = zmq.Context.instance()
        self._default_port = int(default_port)
        self._endpoints = []
        self._sockets = {}
        for r in receivers:
            ep = self._normalize_endpoint(r)
            if ep not in self._endpoints:
                self._endpoints.append(ep)
        for ep in self._endpoints:
            sock = self._ctx.socket(zmq.PUSH)
            sock.setsockopt(zmq.LINGER, 0)
            sock.connect(ep)
            self._sockets[ep] = sock

    def __call__(self, data):
        '''Send data.'''
        results = {}
        for ep in self._endpoints:
            results[ep] = self._send_to_address(ep, data)
        return results

    def _send_to_address(self, address, data, timeout=10):
        '''Send data to address and port without verification of response.'''
        sock = self._sockets.get(address)
        if sock is None:
            # Late-bind socket if not present
            sock = self._ctx.socket(zmq.PUSH)
            sock.setsockopt(zmq.LINGER, 0)
            sock.connect(address)
            self._sockets[address] = sock
            if address not in self._endpoints:
                self._endpoints.append(address)

        # Serialize
        if isinstance(data, (bytes, bytearray, memoryview)):
            payload = bytes(data)
        elif isinstance(data, str):
            payload = data.encode('utf-8')
        else:
            payload = pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)

        # Set send timeout (milliseconds)
        prev_timeout = sock.getsockopt(zmq.SNDTIMEO)
        try:
            sock.setsockopt(zmq.SNDTIMEO, int(timeout * 1000))
            sock.send(payload, flags=0)
            return True
        except zmq.Again:
            return False
        finally:
            # Restore previous timeout
            try:
                sock.setsockopt(zmq.SNDTIMEO, prev_timeout)
            except Exception:
                pass

    def close(self):
        '''Close the sender.'''
        for sock in self._sockets.values():
            try:
                sock.close(0)
            except Exception:
                pass
        self._sockets.clear()
        self._endpoints.clear()
        try:
            # Do not terminate global instance context; just flush
            self._ctx.term()
        except Exception:
            pass

    def _normalize_endpoint(self, receiver):
        r = str(receiver).strip()
        if '://' in r:
            return r
        if ':' in r:
            host, port = r.rsplit(':', 1)
            return f"tcp://{host}:{int(port)}"
        return f"tcp://{r}:{self._default_port}"
