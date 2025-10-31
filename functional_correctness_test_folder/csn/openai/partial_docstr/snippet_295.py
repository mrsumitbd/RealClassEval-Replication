
import socket
from typing import Iterable, Tuple, Union, List, Dict, Any


class DesignatedReceiversSender:
    """
    A simple UDP sender that can send data to a list of designated receivers.
    Each receiver is specified as a host or a (host, port) tuple. If a port
    is not provided, ``default_port`` is used.
    """

    def __init__(self, default_port: int, receivers: Union[Iterable[Union[str, Tuple[str, int]]], Dict[str, int]]):
        """
        Parameters
        ----------
        default_port : int
            The default port to use when a receiver does not specify one.
        receivers : iterable or dict
            Either an iterable of host strings or (host, port) tuples, or a
            mapping from host to port.
        """
        self.default_port = default_port
        self._sockets: List[Tuple[socket.socket, Tuple[str, int]]] = []

        # Normalise receivers into a list of (host, port) tuples
        if isinstance(receivers, dict):
            items = receivers.items()
        else:
            items = receivers

        for item in items:
            if isinstance(item, tuple):
                host, port = item
            else:
                host = item
                port = self.default_port
            # Create a UDP socket for each receiver
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._sockets.append((sock, (host, port)))

    def __call__(self, data: Union[bytes, str]) -> None:
        """
        Send the given data to all designated receivers.

        Parameters
        ----------
        data : bytes or str
            The data to send. If a string is provided, it will be encoded
            using UTF-8.
        """
        if isinstance(data, str):
            data = data.encode("utf-8")

        for sock, addr in self._sockets:
            try:
                sock.sendto(data, addr)
            except Exception:
                # Silently ignore send errors to keep the sender robust
                pass

    def close(self) -> None:
        """Close all sockets used by the sender."""
        for sock, _ in self._sockets:
            try:
                sock.close()
            except Exception:
                pass
        self._sockets.clear()
