
import socket
import threading
import time


class NameServer:
    '''The name server.'''

    def __init__(self, max_age=None, multicast_enabled=True, restrict_to_localhost=False):
        '''Initialize nameserver.'''
        self.max_age = max_age
        self.multicast_enabled = multicast_enabled
        self.restrict_to_localhost = restrict_to_localhost
        self._registry = {}          # name -> (address, timestamp)
        self._running = False
        self._sock = None
        self._thread = None

    def run(self, address_receiver=None, nameserver_address=('0.0.0.0', 5353)):
        '''Run the listener and answer to requests.'''
        if self._running:
            return
        self._running = True

        # Create UDP socket
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind(nameserver_address)

        # Join multicast group if enabled and address is multicast
        if self.multicast_enabled:
            maddr = nameserver_address[0]
            if maddr.startswith('224.') or maddr.startswith('239.'):
                mreq = socket.inet_aton(maddr) + socket.inet_aton('0.0.0.0')
                self._sock.setsockopt(
                    socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        def _loop():
            while self._running:
                try:
                    data, addr = self._sock.recvfrom(4096)
                except OSError:
                    break  # socket closed

                if self.restrict_to_localhost and addr[0] != '127.0.0.1':
                    continue

                try:
                    msg = data.decode().strip()
                except UnicodeDecodeError:
                    continue

                parts = msg.split()
                if not parts:
                    continue

                cmd = parts[0].upper()
                if cmd == 'REGISTER' and len(parts) >= 3:
                    name = parts[1]
                    address = parts[2]
                    self._registry[name] = (address, time.time())
                    self._sock.sendto(b'OK', addr)
                elif cmd == 'LOOKUP' and len(parts) >= 2:
                    name = parts[1]
                    entry = self._registry.get(name)
                    if entry and (self.max_age is None or time.time() - entry[1] <= self.max_age):
                        resp = entry[0]
                    else:
                        resp = 'NOTFOUND'
                    self._sock.sendto(resp.encode(), addr)
                elif cmd == 'UNREGISTER' and len(parts) >= 2:
                    name = parts[1]
                    self._registry.pop(name, None)
                    self._sock.sendto(b'OK', addr)
                else:
                    self._sock.sendto(b'ERROR', addr)

                # Optional callback
                if address_receiver:
                    try:
                        address_receiver(msg, addr)
                    except Exception:
                        pass

        self._thread = threading.Thread(target=_loop, daemon=True)
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
            self._thread.join(timeout=1)
            self._thread = None
