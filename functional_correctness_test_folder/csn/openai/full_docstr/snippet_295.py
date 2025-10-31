
import socket
from typing import Iterable, Tuple, Union, Dict, Any


class DesignatedReceiversSender:
    '''Sends message to multiple *receivers* on *port*.'''

    def __init__(self, default_port: int, receivers: Iterable[Union[str, Tuple[str, int], Dict[str, int]]]):
        '''Set settings.'''
        self.default_port = default_port
        # Normalize receivers into a list of (host, port) tuples
        self._receivers: list[Tuple[str, int]] = []

        for r in receivers:
            if isinstance(r, str):
                # Just a hostname, use default port
                self._receivers.append((r, self.default_port))
            elif isinstance(r, tuple) and len(r) == 2:
                host, port = r
                self._receivers.append((host, int(port)))
            elif isinstance(r, dict):
                # dict mapping host to port
                for host, port in r.items():
                    self._receivers.append((host, int(port)))
            else:
                raise TypeError(f"Unsupported receiver type: {r!r}")

        # Create a single UDP socket for all sends
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __call__(self, data: Union[bytes, str]) -> None:
        '''Send messages from all receivers.'''
        if isinstance(data, str):
            data = data.encode('utf-8')
        for host, port in self._receivers:
            try:
                self._sock.sendto(data, (host, port))
            except Exception as exc:
                # Log or ignore; for now just re-raise
                raise RuntimeError(
                    f"Failed to send to {(host, port)}: {exc}") from exc

    def close(self) -> None:
        '''Close the sender.'''
        try:
            self._sock.close()
        except Exception:
            pass
