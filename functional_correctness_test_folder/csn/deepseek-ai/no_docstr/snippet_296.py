
import socket
import threading
import time
from typing import Optional, Callable


class NameServer:

    def __init__(self, max_age: Optional[int] = None, multicast_enabled: bool = True, restrict_to_localhost: bool = False):
        self.max_age = max_age
        self.multicast_enabled = multicast_enabled
        self.restrict_to_localhost = restrict_to_localhost
        self._running = False
        self._socket = None
        self._thread = None
        self._stop_event = threading.Event()

    def run(self, address_receiver: Optional[Callable] = None, nameserver_address: Optional[str] = None):
        if self._running:
            return

        self._running = True
        self._stop_event.clear()

        def _run_server():
            try:
                self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self._socket.setsockopt(
                    socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

                if self.restrict_to_localhost:
                    host = '127.0.0.1'
                else:
                    host = '0.0.0.0'

                if nameserver_address is not None:
                    port = int(nameserver_address.split(':')[-1])
                else:
                    port = 0  # Let OS assign a free port

                self._socket.bind((host, port))

                if address_receiver is not None:
                    actual_port = self._socket.getsockname()[1]
                    address_receiver(f"{host}:{actual_port}")

                while not self._stop_event.is_set():
                    try:
                        data, addr = self._socket.recvfrom(1024)
                        if self.multicast_enabled:
                            self._socket.sendto(data, addr)
                    except socket.timeout:
                        pass
                    except OSError:
                        break
            finally:
                if self._socket:
                    self._socket.close()

        self._thread = threading.Thread(target=_run_server, daemon=True)
        self._thread.start()

    def stop(self):
        if not self._running:
            return

        self._stop_event.set()
        self._running = False

        if self._socket:
            try:
                self._socket.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            self._socket.close()

        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1)
