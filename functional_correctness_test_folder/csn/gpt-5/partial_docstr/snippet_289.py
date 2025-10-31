import zmq
import json
import pickle


class ZMQDesignatedReceiversSender:
    '''Sends message to multiple *receivers* on *port*.'''

    def __init__(self, default_port, receivers):
        '''Set up the sender.'''
        self._default_port = int(default_port)
        self._context = zmq.Context()
        self._sockets = {}
        self._addresses = []

        for receiver in receivers or []:
            addr = self._normalize_address(receiver)
            if addr in self._sockets:
                continue
            sock = self._context.socket(zmq.PUSH)
            # Avoid hanging forever on close/send
            sock.setsockopt(zmq.LINGER, 0)
            # Sensible high-water mark to buffer some messages but avoid memory blow-up
            sock.setsockopt(zmq.SNDHWM, 1000)
            sock.connect(addr)
            self._sockets[addr] = sock
            self._addresses.append(addr)

    def __call__(self, data):
        '''Send data.'''
        payload = self._serialize(data)
        results = {}
        for addr in self._addresses:
            results[addr] = self._send_to_address(addr, payload, timeout=10)
        return results

    def _send_to_address(self, address, data, timeout=10):
        sock = self._sockets.get(address)
        if sock is None:
            return False
        try:
            # Temporarily set timeout for this send
            prev_timeout = sock.getsockopt(zmq.SNDTIMEO)
        except Exception:
            prev_timeout = None
        try:
            sock.setsockopt(zmq.SNDTIMEO, int(timeout * 1000))
            sock.send(data)
            return True
        except zmq.Again:
            return False
        except Exception:
            return False
        finally:
            if prev_timeout is not None:
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
        try:
            self._context.term()
        except Exception:
            pass

    def _normalize_address(self, receiver):
        r = str(receiver).strip()
        if "://" in r:
            return r
        if ":" in r:
            return f"tcp://{r}"
        return f"tcp://{r}:{self._default_port}"

    def _serialize(self, data):
        if isinstance(data, (bytes, bytearray, memoryview)):
            return bytes(data)
        if isinstance(data, str):
            return data.encode("utf-8")
        try:
            return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        except Exception:
            return pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)
