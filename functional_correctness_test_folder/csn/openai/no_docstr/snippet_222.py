
import socket
import time
from typing import Any, Callable, Tuple, Optional


class Transport:
    """
    A simple transport wrapper that manages a socket connection.

    Parameters
    ----------
    gateway : Tuple[str, int]
        The host and port to connect to.
    connect : Callable[[Tuple[str, int], **Any], socket.socket]
        A callable that returns a connected socket. It should accept the
        gateway tuple as the first positional argument and any additional
        keyword arguments.
    timeout : float, optional
        Timeout in seconds for socket operations. Default is 1.0.
    reconnect_timeout : float, optional
        Seconds to wait before attempting to reconnect after a failure.
        Default is 10.0.
    **kwargs
        Additional keyword arguments forwarded to the `connect` callable.
    """

    def __init__(
        self,
        gateway: Tuple[str, int],
        connect: Callable[[Tuple[str, int], **Any], socket.socket],
        timeout: float = 1.0,
        reconnect_timeout: float = 10.0,
        **kwargs: Any,
    ) -> None:
        self.gateway = gateway
        self.connect = connect
        self.timeout = timeout
        self.reconnect_timeout = reconnect_timeout
        self._connect_kwargs = kwargs
        self._sock: Optional[socket.socket] = None
        self._connect()

    def _connect(self) -> None:
        """Establish a new socket connection."""
        if self._sock:
            try:
                self._sock.close()
            except Exception:
                pass
            self._sock = None

        try:
            self._sock = self.connect(self.gateway, **self._connect_kwargs)
            if self._sock:
                self._sock.settimeout(self.timeout)
        except Exception as exc:
            raise ConnectionError(
                f"Failed to connect to {self.gateway}: {exc}") from exc

    def disconnect(self) -> None:
        """Close the current socket connection."""
        if self._sock:
            try:
                self._sock.shutdown(socket.SHUT_RDWR)
            except Exception:
                pass
            try:
                self._sock.close()
            except Exception:
                pass
            finally:
                self._sock = None

    def send(self, message: Any) -> None:
        """
        Send a message over the transport.

        Parameters
        ----------
        message : Any
            The data to send. If a string, it will be encoded to UTF-8 bytes.
            Otherwise, it must be a bytes-like object.
        """
        if not self._sock:
            self._connect()

        data: bytes
        if isinstance(message, str):
            data = message.encode("utf-8")
        elif isinstance(message, (bytes, bytearray)):
            data = bytes(message)
        else:
            raise TypeError("Message must be str, bytes, or bytearray")

        try:
            self._sock.sendall(data)
        except Exception:
            # Attempt to reconnect and resend once
            self.disconnect()
            time.sleep(self.reconnect_timeout)
            self._connect()
            if not self._sock:
                raise ConnectionError(
                    "Reconnection failed; cannot send message")
            try:
                self._sock.sendall(data)
            except Exception as exc:
                raise ConnectionError(
                    f"Failed to send message after reconnection: {exc}") from exc
