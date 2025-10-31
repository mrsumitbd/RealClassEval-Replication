
import socket
from typing import Iterable, Tuple, Union, List, Optional


class DesignatedReceiversSender:
    """
    A simple TCP sender that connects to a list of designated receivers
    (host, port) pairs and sends data to all of them when called.
    """

    def __init__(self, default_port: int, receivers: Iterable[Union[str, Tuple[str, int]]]):
        """
        Parameters
        ----------
        default_port : int
            The port to use when a receiver is specified only by hostname.
        receivers : Iterable[Union[str, Tuple[str, int]]]
            An iterable of receiver specifications. Each element can be:
            * a string hostname (port will be taken from ``default_port``)
            * a tuple/list ``(hostname, port)``

        Raises
        ------
        ValueError
            If a receiver specification is invalid.
        """
        self._default_port = default_port
        self._sockets: List[socket.socket] = []

        for r in receivers:
            if isinstance(r, (list, tuple)):
                if len(r) != 2:
                    raise ValueError(
                        f"Receiver tuple must be (host, port), got {r!r}")
                host, port = r
            elif isinstance(r, str):
                host = r
                port = default_port
            else:
                raise ValueError(f"Unsupported receiver type: {type(r)}")

            try:
                # Create a TCP socket and connect
                s = socket.create_connection((host, port))
                self._sockets.append(s)
            except Exception as exc:
                # If a connection fails, we skip this receiver but keep the rest
                # Optionally, you could log the error here
                continue

    def __call__(self, data: Union[bytes, str]) -> None:
        """
        Send the given data to all connected receivers.

        Parameters
        ----------
        data : bytes or str
            The data to send. If a string is provided, it will be encoded
            using UTF-8 before sending.

        Raises
        ------
        RuntimeError
            If no receivers are connected.
        """
        if not self._sockets:
            raise RuntimeError("No receivers are connected")

        if isinstance(data, str):
            payload = data.encode("utf-8")
        else:
            payload = data

        # Send to each socket; if a send fails, close that socket
        dead_sockets = []
        for s in self._sockets:
            try:
                s.sendall(payload)
            except Exception:
                dead_sockets.append(s)

        for s in dead_sockets:
            try:
                s.close()
            finally:
                self._sockets.remove(s)

    def close(self) -> None:
        """
        Close all open sockets.
        """
        for s in self._sockets:
            try:
                s.close()
            except Exception:
                pass
        self._sockets.clear()
