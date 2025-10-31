
import threading
import socket
import time


class NameServer:

    def __init__(self, max_age=None, multicast_enabled=True, restrict_to_localhost=False):
        self.max_age = max_age
        self.multicast_enabled = multicast_enabled
        self.restrict_to_localhost = restrict_to_localhost
        self._running = False
        self._thread = None
        self._sock = None
        self._nameserver_address = None

    def _serve(self, address_receiver):
        # Use UDP socket for demonstration
        if self.restrict_to_localhost:
            bind_addr = ('127.0.0.1', 0)
        else:
            bind_addr = ('', 0)
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind(bind_addr)
        self._nameserver_address = self._sock.getsockname()
        if address_receiver:
            address_receiver(self._nameserver_address)
        start_time = time.time()
        self._running = True
        while self._running:
            self._sock.settimeout(0.5)
            try:
                data, addr = self._sock.recvfrom(1024)
                # Echo back for demonstration
                self._sock.sendto(b'OK', addr)
            except socket.timeout:
                pass
            if self.max_age is not None and (time.time() - start_time) > self.max_age:
                break
        self._sock.close()
        self._sock = None

    def run(self, address_receiver=None, nameserver_address=None):
        if self._running:
            return
        self._thread = threading.Thread(
            target=self._serve, args=(address_receiver,))
        self._thread.daemon = True
        self._thread.start()
        # Wait for the server to start and bind
        while self._nameserver_address is None and self._thread.is_alive():
            time.sleep(0.01)

    def stop(self):
        self._running = False
        if self._sock:
            try:
                # Send dummy packet to unblock recvfrom
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.sendto(b'', self._nameserver_address)
                s.close()
            except Exception:
                pass
        if self._thread:
            self._thread.join()
            self._thread = None
        self._nameserver_address = None
