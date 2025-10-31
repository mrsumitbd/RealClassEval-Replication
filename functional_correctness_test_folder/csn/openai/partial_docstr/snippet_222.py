
import socket
import time


class Transport:
    '''Handle gateway transport.
    I/O is allowed in this class. This class should host methods that
    are related to the gateway transport type.
    '''

    def __init__(self, gateway, connect, timeout=1.0, reconnect_timeout=10.0, **kwargs):
        """
        Parameters
        ----------
        gateway : any
            Information needed by the `connect` callable to establish a connection
            (e.g. a (host, port) tuple for a TCP socket).
        connect : callable
            A function that returns a connected socket-like object when called
            with `gateway` and any additional keyword arguments.
        timeout : float, optional
            Timeout in seconds for socket operations.
        reconnect_timeout : float, optional
            Seconds to wait before attempting to reconnect after a failure.
        **kwargs : dict
            Additional keyword arguments forwarded to `connect`.
        """
        self.gateway = gateway
        self.connect = connect
        self.timeout = timeout
        self.reconnect_timeout = reconnect_timeout
        self.kwargs = kwargs
        self._sock = None
        self._connect()

    def _connect(self):
        """Establish a new connection using the provided connect callable."""
        if self._sock:
            self.disconnect()
        try:
            self._sock = self.connect(self.gateway, **self.kwargs)
            self._sock.settimeout(self.timeout)
        except Exception as exc:
            self._sock = None
            raise RuntimeError(
                f"Failed to connect to {self.gateway!r}") from exc

    def disconnect(self):
        '''Disconnect from the transport.'''
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

    def send(self, message):
        '''Write a message to the gateway.'''
        if not self._sock:
            self._connect()
        try:
            data = message if isinstance(
                message, (bytes, bytearray)) else message.encode('utf-8')
            self._sock.sendall(data)
        except Exception:
            # Attempt a single reconnect and retry once
            self.disconnect()
            time.sleep(self.reconnect_timeout)
            self._connect()
            if not self._sock:
                raise RuntimeError("Unable to reconnect to gateway")
            data = message if isinstance(
                message, (bytes, bytearray)) else message.encode('utf-8')
            self._sock.sendall(data)
