import selectors
from typing import Iterable, Tuple, List, Optional


class SocketReceiver:

    def __init__(self):
        self._selector = selectors.DefaultSelector()
        self._registered = set()

    def register(self, socket):
        if socket in self._registered:
            return
        try:
            self._selector.register(socket, selectors.EVENT_READ)
            self._registered.add(socket)
        except KeyError:
            # Already registered in selector; keep state consistent
            self._registered.add(socket)

    def unregister(self, socket):
        if socket in self._registered:
            try:
                self._selector.unregister(socket)
            except Exception:
                pass
            finally:
                self._registered.discard(socket)

    def _select_and_recv(self, sel: selectors.BaseSelector, timeout: Optional[float]) -> List[Tuple[object, bytes]]:
        ready = sel.select(timeout)
        results: List[Tuple[object, bytes]] = []
        for key, _ in ready:
            sock = key.fileobj
            try:
                data = sock.recv(4096)
            except BlockingIOError:
                continue
            except InterruptedError:
                continue
            except Exception:
                # On unexpected errors, treat as closed
                data = b""
            if sel is self._selector and data == b"":
                # If connection closed, unregister from persistent selector
                self.unregister(sock)
            results.append((sock, data))
        return results

    def receive(self, *sockets, timeout=None):
        if sockets:
            temp_sel = selectors.DefaultSelector()
            try:
                # Allow iterables passed directly or multiple args
                socks: Iterable = sockets
                if len(sockets) == 1 and hasattr(sockets[0], "__iter__") and not hasattr(sockets[0], "recv"):
                    socks = sockets[0]
                for s in socks:
                    try:
                        temp_sel.register(s, selectors.EVENT_READ)
                    except Exception:
                        continue
                return self._select_and_recv(temp_sel, timeout)
            finally:
                temp_sel.close()
        else:
            if not self._registered:
                return []
            return self._select_and_recv(self._selector, timeout)
