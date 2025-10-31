import zmq
import socket
import pickle
from typing import Any, Dict, Iterable, Tuple, Union


class ZMQDesignatedReceiversSender:

    def __init__(self, default_port: int, receivers: Union[Dict[Any, Any], Iterable[Any]]):
        self._ctx = zmq.Context.instance()
        self._default_port = int(default_port)
        self._closed = False
        self._receivers = self._normalize_receivers(receivers)

    def __call__(self, data):
        if self._closed:
            raise RuntimeError("Sender is closed")
        # data can be:
        # - dict: {receiver_key: payload}
        # - tuple: (receiver_key, payload[, timeout])
        # - any payload: broadcast to all
        if isinstance(data, dict):
            for key, payload in data.items():
                address = self._receivers.get(key)
                if address is None:
                    raise KeyError(f"Unknown receiver '{key}'")
                self._send_to_address(address, payload)
            return
        if isinstance(data, tuple):
            if len(data) not in (2, 3):
                raise ValueError(
                    "Tuple form must be (receiver_key, payload[, timeout])")
            key, payload = data[0], data[1]
            timeout = data[2] if len(data) == 3 else 10
            address = self._receivers.get(key)
            if address is None:
                raise KeyError(f"Unknown receiver '{key}'")
            self._send_to_address(address, payload, timeout=timeout)
            return
        # broadcast
        for address in self._receivers.values():
            self._send_to_address(address, data)

    def _send_to_address(self, address, data, timeout=10):
        if self._closed:
            raise RuntimeError("Sender is closed")
        endpoint = self._normalize_endpoint(address)
        sock = self._ctx.socket(zmq.REQ)
        try:
            # timeouts in milliseconds
            ms = max(0, int(timeout * 1000))
            sock.setsockopt(zmq.LINGER, 0)
            sock.setsockopt(zmq.SNDTIMEO, ms)
            sock.setsockopt(zmq.RCVTIMEO, ms)
            sock.connect(endpoint)
            payload = self._serialize(data)
            sock.send(payload)
            # Expect a simple acknowledgement; if no reply within timeout, raise
            try:
                _ = sock.recv()
            except zmq.Again:
                raise TimeoutError(
                    f"Timed out waiting for reply from {endpoint}")
        finally:
            sock.close(0)

    def close(self):
        if self._closed:
            return
        self._closed = True
        # Do not terminate the shared instance context globally for other users.
        # Create our own context if strict termination is needed.
        # Here, gracefully create a dummy socket to ensure context is alive until now.
        # No additional resources to release because sockets are per-send.
        pass

    def _normalize_receivers(self, receivers: Union[Dict[Any, Any], Iterable[Any]]) -> Dict[Any, str]:
        normalized: Dict[Any, str] = {}
        if isinstance(receivers, dict):
            items = receivers.items()
        else:
            # iterable of addresses; key them by index
            items = enumerate(receivers)
        for key, value in items:
            normalized[key] = self._normalize_endpoint(value)
        return normalized

    def _normalize_endpoint(self, address: Any) -> str:
        # Accept:
        # - full endpoint like "tcp://host:port" or "ipc://..."
        # - tuple (host, port)
        # - "host" -> tcp://host:default_port
        # - "host:port"
        if isinstance(address, tuple) and len(address) == 2:
            host, port = address
            return f"tcp://{host}:{int(port)}"
        if isinstance(address, str):
            addr = address.strip()
            if "://" in addr:
                return addr
            if ":" in addr:
                host, port = addr.rsplit(":", 1)
                return f"tcp://{host}:{int(port)}"
            return f"tcp://{addr}:{self._default_port}"
        # Fallback to str()
        s = str(address)
        if "://" in s:
            return s
        if ":" in s:
            host, port = s.rsplit(":", 1)
            return f"tcp://{host}:{int(port)}"
        return f"tcp://{s}:{self._default_port}"

    def _serialize(self, data: Any) -> bytes:
        if isinstance(data, (bytes, bytearray, memoryview)):
            return bytes(data)
        if isinstance(data, str):
            return data.encode("utf-8")
        try:
            return pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            raise TypeError(
                f"Unable to serialize data of type {type(data).__name__}") from e
