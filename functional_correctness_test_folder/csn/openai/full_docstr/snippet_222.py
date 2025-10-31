
import time
import socket
from typing import Any, Callable, Optional


class Transport:
    '''Handle gateway transport.
    I/O is allowed in this class. This class should host methods that
    are related to the gateway transport type.
    '''

    def __init__(
        self,
        gateway: Any,
        connect: Callable[..., Any],
        timeout: float = 1.0,
        reconnect_timeout: float = 10.0,
        **kwargs: Any,
    ):
        '''Set up transport.'''
        self.gateway = gateway
        self.connect = connect
        self.timeout = timeout
        self.reconnect_timeout = reconnect_timeout
        self.kwargs = kwargs

        # Attempt initial connection
        self._conn: Optional[Any] = None
        self._connect()

    def _connect(self) -> None:
        '''Internal helper to establish a connection.'''
        try:
            self._conn = self.connect(self.gateway, **self.kwargs)
            # If the returned object is a socket, set its timeout
            if hasattr(self._conn, "settimeout"):
                self._conn.settimeout(self.timeout)
        except Exception as exc:
            raise ConnectionError(f"Failed to connect: {exc}") from exc

    def disconnect(self) -> None:
        '''Disconnect from the transport.'''
        if self._conn:
            try:
                # Try graceful close if possible
                if hasattr(self._conn, "shutdown"):
                    try:
                        self._conn.shutdown(socket.SHUT_RDWR)
                    except Exception:
                        pass
                if hasattr(self._conn, "close"):
                    self._conn.close()
            finally:
                self._conn = None

    def send(self, message: bytes) -> None:
        '''Write a message to the gateway.'''
        if not isinstance(message, (bytes, bytearray)):
            raise TypeError("message must be bytes or bytearray")

        if not self._conn:
            self._connect()

        try:
            # Use sendall to ensure full message is sent
            self._conn.sendall(message)
        except (BrokenPipeError, ConnectionResetError, socket.timeout) as exc:
            # Attempt to reconnect once and resend
            self.disconnect()
            time.sleep(self.reconnect_timeout)
            self._connect()
            try:
                self._conn.sendall(message)
            except Exception as e2:
                raise ConnectionError(
                    f"Send failed after reconnect: {e2}") from e2
        except Exception as exc:
            raise ConnectionError(f"Send failed: {exc}") from exc
