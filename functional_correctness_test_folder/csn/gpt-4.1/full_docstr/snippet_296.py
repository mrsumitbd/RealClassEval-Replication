
import threading
import socket
import time
import struct


class NameServer:
    '''The name server.'''

    MULTICAST_GROUP = '224.0.0.251'
    MULTICAST_PORT = 5353
    DEFAULT_PORT = 5353

    def __init__(self, max_age=None, multicast_enabled=True, restrict_to_localhost=False):
        '''Initialize nameserver.'''
        self.max_age = max_age
        self.multicast_enabled = multicast_enabled
        self.restrict_to_localhost = restrict_to_localhost
        self._running = False
        self._thread = None
        self._sock = None

    def run(self, address_receiver=None, nameserver_address=None):
        '''Run the listener and answer to requests.'''
        if self._running:
            return
        self._running = True

        def server_loop():
            if nameserver_address is None:
                if self.multicast_enabled:
                    bind_addr = ('', self.MULTICAST_PORT)
                else:
                    bind_addr = (
                        '127.0.0.1' if self.restrict_to_localhost else '', self.DEFAULT_PORT)
            else:
                bind_addr = nameserver_address

            self._sock = socket.socket(
                socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                self._sock.bind(bind_addr)
            except Exception:
                self._running = False
                return

            if self.multicast_enabled:
                mreq = struct.pack("4sl", socket.inet_aton(
                    self.MULTICAST_GROUP), socket.INADDR_ANY)
                self._sock.setsockopt(
                    socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

            start_time = time.time()
            while self._running:
                try:
                    self._sock.settimeout(1.0)
                    try:
                        data, addr = self._sock.recvfrom(1024)
                    except socket.timeout:
                        data, addr = None, None
                    if data:
                        if address_receiver:
                            address_receiver(addr)
                        # Echo back for demonstration
                        self._sock.sendto(b'OK', addr)
                    if self.max_age is not None and (time.time() - start_time) > self.max_age:
                        break
                except Exception:
                    break
            self._sock.close()
            self._sock = None
            self._running = False

        self._thread = threading.Thread(target=server_loop, daemon=True)
        self._thread.start()

    def stop(self):
        '''Stop the nameserver.'''
        self._running = False
        if self._sock:
            try:
                self._sock.close()
            except Exception:
                pass
            self._sock = None
        if self._thread:
            self._thread.join(timeout=2)
            self._thread = None
