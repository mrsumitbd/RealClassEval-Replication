
import select
import socket
from typing import Iterable, List, Tuple, Optional


class SocketReceiver:
    """
    A simple socket receiver that can register sockets, unregister them,
    and wait for any of them to become readable. The `receive` method
    returns a list of (socket, data) tuples for all sockets that are
    ready to read.
    """

    def __init__(self) -> None:
        # Store registered sockets in a set for quick lookup
        self._registered: set[socket.socket] = set()

    def register(self, sock: socket.socket) -> None:
        """
        Register a socket to be monitored for readability.
        """
        if not isinstance(sock, socket.socket):
            raise TypeError("Only socket.socket instances can be registered")
        self._registered.add(sock)

    def unregister(self, sock: socket.socket) -> None:
        """
        Unregister a previously registered socket.
        """
        self._registered.discard(sock)

    def _get_sockets(self, sockets: Iterable[socket.socket]) -> List[socket.socket]:
        """
        Resolve the list of sockets to monitor. If no sockets are provided,
        use all registered sockets. Otherwise, filter the provided sockets
        to those that are registered.
        """
        if not sockets:
            return list(self._registered)
        # Ensure all provided sockets are registered
        filtered = [s for s in sockets if s in self._registered]
        if not filtered:
            raise ValueError("No registered sockets provided to receive")
        return filtered

    def receive(
        self,
        *sockets: socket.socket,
        timeout: Optional[float] = None,
    ) -> List[Tuple[socket.socket, bytes]]:
        """
        Wait for any of the specified sockets (or all registered sockets if none
        are specified) to become readable. Returns a list of (socket, data)
        tuples for each socket that has data ready to be read.

        Parameters
        ----------
        *sockets : socket.socket
            Optional sockets to monitor. If omitted, all registered sockets
            are monitored.
        timeout : float, optional
            Timeout in seconds. If None, block indefinitely.

        Returns
        -------
        List[Tuple[socket.socket, bytes]]
            A list of tuples containing the socket and the data read from it.
            If no sockets are ready, returns an empty list.
        """
        # Resolve sockets to monitor
        monitor_socks = self._get_sockets(sockets)

        if not monitor_socks:
            return []

        # Use select to wait for readability
        try:
            ready, _, _ = select.select(monitor_socks, [], [], timeout)
        except (ValueError, OSError) as exc:
            # If select fails (e.g., invalid socket), raise a clear error
            raise RuntimeError(f"Select failed: {exc}") from exc

        results: List[Tuple[socket.socket, bytes]] = []

        for sock in ready:
            try:
                # Read up to 4096 bytes; adjust as needed
                data = sock.recv(4096)
                if data:
                    results.append((sock, data))
                else:
                    # No data means the socket has been closed; unregister it
                    self.unregister(sock)
            except BlockingIOError:
                # Non-blocking socket had no data; ignore
                continue
            except OSError as exc:
                # On error, unregister the socket and skip
                self.unregister(sock)
                continue

        return results
