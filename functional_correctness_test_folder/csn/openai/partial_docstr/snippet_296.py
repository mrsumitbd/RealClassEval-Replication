
import socket
import struct
import threading
import time


class NameServer:
    '''The name server.'''

    # Default mDNS multicast address and port
    MDNS_GROUP = '224.0.0.251'
    MDNS_PORT = 5353

    def __init__(self, max_age=None, multicast_enabled=True, restrict_to_localhost=False):
        """
        Parameters
        ----------
        max_age : int or None
            Maximum age (TTL) for responses in seconds. Not used in this simple implementation.
        multicast_enabled : bool
            If True, join the mDNS multicast group.
        restrict_to_localhost : bool
            If True, bind only to the loopback interface.
        """
        self.max_age = max_age
        self.multicast_enabled = multicast_enabled
        self.restrict_to_localhost = restrict_to_localhost

        self._sock = None
        self._thread = None
        self._stop_event = threading.Event()

    def run(self, address_receiver=None, nameserver_address=None):
        """
        Start the name server.

        Parameters
        ----------
        address_receiver : callable or None
            A callable that receives (data, addr) tuples from the socket.
            If None, data is simply discarded.
        nameserver_address : tuple or None
            Address to bind to. If None, defaults to ('0.0.0.0', MDNS_PORT)
            or ('127.0.0.1', MDNS_PORT) if restrict_to_localhost is True.
        """
        if self._sock is not None:
            raise RuntimeError("NameServer is already running")

        # Determine bind address
        if nameserver_address is None:
            host = '127.0.0.1' if self.restrict_to_localhost else '0.0.0.0'
            nameserver_address = (host, self.MDNS_PORT)

        # Create UDP socket
        self._sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # Allow multiple sockets to use the same PORT number
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind to the address
        self._sock.bind(nameserver_address)

        if self.multicast_enabled:
            # Join multicast group
            mreq = struct.pack("4sl", socket.inet_aton(
                self.MDNS_GROUP), socket.INADDR_ANY)
            self._sock.setsockopt(
                socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        # Start listener thread
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._listen_loop, args=(address_receiver,), daemon=True)
        self._thread.start()

    def _listen_loop(self, address_receiver):
        """Internal method: loop receiving data and calling the receiver."""
        while not self._stop_event.is_set():
            try:
                self._sock.settimeout(0.5)
                data, addr = self._sock.recvfrom(65535)
                if address_receiver:
                    try:
                        address_receiver(data, addr)
                    except Exception:
                        # Ignore errors in the receiver to keep the server running
                        pass
            except socket.timeout:
                continue
            except OSError:
                break

    def stop(self):
        """Stop the name server and close the socket."""
        if self._sock is None:
            return
        self._stop_event.set()
        # Closing the socket will unblock recvfrom
        try:
            self._sock.close()
        except OSError:
            pass
        self._sock = None
        if self._thread is not None:
            self._thread.join(timeout=1.0)
            self._thread = None
