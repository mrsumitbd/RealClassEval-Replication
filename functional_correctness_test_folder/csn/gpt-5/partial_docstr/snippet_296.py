import socket
import struct
import threading
import time
import select


class NameServer:
    '''The name server.'''

    _MULTICAST_GRP = '239.255.42.42'
    _MULTICAST_PORT = 42424
    _ANNOUNCE_INTERVAL = 2.0
    _RECV_BUFSIZE = 65535

    def __init__(self, max_age=None, multicast_enabled=True, restrict_to_localhost=False):
        self.max_age = max_age
        self.multicast_enabled = multicast_enabled
        self.restrict_to_localhost = restrict_to_localhost

        self._thread = None
        self._stop_evt = threading.Event()
        self._lock = threading.RLock()

        self._unicast_sock = None
        self._mc_recv_sock = None

        self._address = None  # (host, port) bound for unicast
        self._address_receiver = None

        self._peers = {}  # {(host, port): last_seen_epoch}

    def run(self, address_receiver=None, nameserver_address=None):
        with self._lock:
            if self._thread and self._thread.is_alive():
                return
            self._address_receiver = address_receiver
            self._setup_sockets(nameserver_address)
            self._stop_evt.clear()
            self._thread = threading.Thread(
                target=self._loop, name="NameServer", daemon=True)
            self._thread.start()

    def stop(self):
        with self._lock:
            self._stop_evt.set()
            t = self._thread
        if t:
            t.join(timeout=5.0)
        self._close_sockets()

    # Internal methods

    def _setup_sockets(self, nameserver_address):
        host, port = self._parse_address(nameserver_address)
        uc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            uc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except OSError:
            pass
        uc.bind((host, port))
        uc.setblocking(False)
        bound_host = uc.getsockname()[0]
        bound_port = uc.getsockname()[1]
        self._unicast_sock = uc
        self._address = (bound_host, bound_port)

        if self.multicast_enabled and not self.restrict_to_localhost:
            self._mc_recv_sock = self._create_multicast_receiver()
        else:
            self._mc_recv_sock = None

    def _close_sockets(self):
        with self._lock:
            if self._unicast_sock:
                try:
                    self._unicast_sock.close()
                except Exception:
                    pass
                self._unicast_sock = None
            if self._mc_recv_sock:
                try:
                    # Attempt to drop membership
                    mreq = struct.pack("=4s4s", socket.inet_aton(
                        self._MULTICAST_GRP), socket.inet_aton("0.0.0.0"))
                    try:
                        self._mc_recv_sock.setsockopt(
                            socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
                    except OSError:
                        pass
                    self._mc_recv_sock.close()
                except Exception:
                    pass
                self._mc_recv_sock = None

    def _parse_address(self, addr):
        if addr is None:
            host = "127.0.0.1" if self.restrict_to_localhost else ""
            return host, 0
        if isinstance(addr, tuple) and len(addr) == 2:
            return addr[0], int(addr[1])
        if isinstance(addr, str):
            if ":" in addr:
                h, p = addr.rsplit(":", 1)
                return h or ("127.0.0.1" if self.restrict_to_localhost else ""), int(p)
            try:
                # if it's just a port
                return ("127.0.0.1" if self.restrict_to_localhost else ""), int(addr)
            except ValueError:
                return addr, 0
        # Fallback
        return ("127.0.0.1" if self.restrict_to_localhost else ""), 0

    def _create_multicast_receiver(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                          socket.IPPROTO_UDP)
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except OSError:
            pass
        try:
            s.bind(('', self._MULTICAST_PORT))
        except OSError:
            # If bind fails, disable multicast receive
            s.close()
            return None
        mreq = struct.pack("=4s4s", socket.inet_aton(
            self._MULTICAST_GRP), socket.inet_aton("0.0.0.0"))
        try:
            s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        except OSError:
            try:
                s.close()
            finally:
                return None
        s.setblocking(False)
        return s

    def _send_multicast_announcement(self):
        if not self.multicast_enabled or self.restrict_to_localhost:
            return
        if not self._unicast_sock or not self._address:
            return
        msg = self._encode_message(
            "NS", self._address[0], str(self._address[1]))
        try:
            # Send via a dedicated sending socket to set TTL and LOOP
            s = socket.socket(
                socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            try:
                s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
                s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
            except OSError:
                pass
            s.sendto(msg, (self._MULTICAST_GRP, self._MULTICAST_PORT))
        except Exception:
            pass
        finally:
            try:
                s.close()
            except Exception:
                pass

    def _loop(self):
        last_announce = 0.0
        while not self._stop_evt.is_set():
            now = time.time()
            if now - last_announce >= self._ANNOUNCE_INTERVAL:
                self._send_multicast_announcement()
                last_announce = now

            rlist = []
            if self._unicast_sock:
                rlist.append(self._unicast_sock)
            if self._mc_recv_sock:
                rlist.append(self._mc_recv_sock)

            timeout = 0.2
            try:
                readable, _, _ = select.select(rlist, [], [], timeout)
            except Exception:
                readable = []

            for sock in readable:
                try:
                    data, addr = sock.recvfrom(self._RECV_BUFSIZE)
                except Exception:
                    continue
                self._handle_packet(data, addr, sock)

            self._evict_old_peers()

    def _handle_packet(self, data, addr, sock):
        try:
            text = data.decode('utf-8', errors='ignore').strip()
        except Exception:
            return
        if not text:
            return

        parts = text.split()
        if not parts:
            return

        cmd = parts[0].upper()

        if cmd == "DISCOVER":
            self._reply_with_address(addr)
            return

        if cmd == "NS":
            if len(parts) >= 3:
                host = parts[1]
                try:
                    port = int(parts[2])
                except ValueError:
                    return
                self._record_peer((host, port))
            return

        if cmd == "PING":
            self._sendto_safe(b"PONG", addr)
            return

        if cmd == "WHERE":
            if len(parts) >= 2 and parts[1].upper() == "NS":
                self._reply_with_address(addr)
            return

    def _reply_with_address(self, addr):
        if not self._address:
            return
        msg = self._encode_message(
            "NS", self._address[0], str(self._address[1]))
        self._sendto_safe(msg, addr)

    def _sendto_safe(self, data, addr):
        try:
            if self._unicast_sock:
                self._unicast_sock.sendto(data, addr)
        except Exception:
            pass

    def _record_peer(self, peer):
        now = time.time()
        with self._lock:
            self._peers[peer] = now
        cb = self._address_receiver
        if cb:
            try:
                cb(peer)
            except Exception:
                pass

    def _evict_old_peers(self):
        if self.max_age is None:
            return
        cutoff = time.time() - float(self.max_age)
        with self._lock:
            stale = [p for p, ts in self._peers.items() if ts < cutoff]
            for p in stale:
                self._peers.pop(p, None)

    def _encode_message(self, *parts):
        return (" ".join(parts)).encode("utf-8")

    # Optional helpers

    @property
    def address(self):
        return self._address

    @property
    def peers(self):
        with self._lock:
            return dict(self._peers)
