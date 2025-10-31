import json
import socket
import threading
import time
from socketserver import ThreadingMixIn, TCPServer, StreamRequestHandler


class _ThreadingTCPServer(ThreadingMixIn, TCPServer):
    daemon_threads = True
    allow_reuse_address = True


class NameServer:
    '''The name server.'''

    def __init__(self, max_age=None, multicast_enabled=True, restrict_to_localhost=False):
        '''Initialize nameserver.'''
        self.max_age = max_age if (isinstance(
            max_age, (int, float)) and max_age > 0) else None
        self.multicast_enabled = bool(multicast_enabled)
        self.restrict_to_localhost = bool(restrict_to_localhost)

        self._registry = {}  # name -> {"address": str, "time": float, "ttl": float or None}
        self._lock = threading.RLock()

        self._server = None
        self._server_thread = None
        self._cleaner_thread = None
        self._stopping = threading.Event()
        self._started = threading.Event()

    def _purge_expired(self):
        if self.max_age is None:
            return
        now = time.time()
        to_del = []
        with self._lock:
            for name, meta in self._registry.items():
                ttl = meta.get("ttl", None)
                effective_ttl = ttl if ttl is not None else self.max_age
                if effective_ttl is None:
                    continue
                if (now - meta.get("time", 0)) > float(effective_ttl):
                    to_del.append(name)
            for name in to_del:
                self._registry.pop(name, None)

    def _cleaner(self):
        interval = 1.0 if not self.max_age else max(
            1.0, float(self.max_age) / 2.0)
        while not self._stopping.wait(interval):
            self._purge_expired()

    def _make_handler(self):
        outer = self

        class Handler(StreamRequestHandler):
            def handle(self):
                while True:
                    line = self.rfile.readline()
                    if not line:
                        break
                    try:
                        payload = json.loads(line.decode("utf-8").strip())
                    except Exception:
                        self._send({"ok": False, "error": "invalid_json"})
                        continue
                    try:
                        resp = self._process(payload)
                    except Exception as e:
                        self._send(
                            {"ok": False, "error": f"server_error: {e.__class__.__name__}"})
                    else:
                        self._send(resp)

            def _send(self, obj):
                data = (json.dumps(obj, separators=(
                    ",", ":")) + "\n").encode("utf-8")
                self.wfile.write(data)
                self.wfile.flush()

            def _process(self, payload):
                cmd = str(payload.get("cmd", "")).lower()
                if cmd == "ping":
                    return {"ok": True, "result": "pong"}
                if cmd == "register":
                    name = payload.get("name")
                    address = payload.get("address")
                    ttl = payload.get("ttl", None)
                    if not name or not isinstance(name, str) or not address or not isinstance(address, str):
                        return {"ok": False, "error": "invalid_arguments"}
                    if ttl is not None:
                        try:
                            ttl = float(ttl)
                            if ttl <= 0:
                                ttl = None
                        except Exception:
                            ttl = None
                    with outer._lock:
                        outer._registry[name] = {
                            "address": address, "time": time.time(), "ttl": ttl}
                    return {"ok": True}
                if cmd == "lookup":
                    name = payload.get("name")
                    if not name or not isinstance(name, str):
                        return {"ok": False, "error": "invalid_arguments"}
                    outer._purge_expired()
                    with outer._lock:
                        meta = outer._registry.get(name)
                        if not meta:
                            return {"ok": True, "result": None}
                        return {"ok": True, "result": meta["address"]}
                if cmd == "unregister":
                    name = payload.get("name")
                    if not name or not isinstance(name, str):
                        return {"ok": False, "error": "invalid_arguments"}
                    with outer._lock:
                        existed = name in outer._registry
                        outer._registry.pop(name, None)
                    return {"ok": True, "result": bool(existed)}
                if cmd == "list":
                    outer._purge_expired()
                    with outer._lock:
                        items = {k: v["address"]
                                 for k, v in outer._registry.items()}
                    return {"ok": True, "result": items}
                return {"ok": False, "error": "unknown_command"}

        return Handler

    def _normalize_address(self, nameserver_address):
        if nameserver_address is None:
            host = "127.0.0.1" if self.restrict_to_localhost else "0.0.0.0"
            return (host, 0)
        if isinstance(nameserver_address, int):
            host = "127.0.0.1" if self.restrict_to_localhost else "0.0.0.0"
            return (host, int(nameserver_address))
        if isinstance(nameserver_address, str):
            # Accept "host:port" or just host (port=0)
            if ":" in nameserver_address and not nameserver_address.startswith("["):
                host, port = nameserver_address.rsplit(":", 1)
                return (host, int(port))
            return (nameserver_address, 0)
        if isinstance(nameserver_address, (list, tuple)) and len(nameserver_address) == 2:
            return (str(nameserver_address[0]), int(nameserver_address[1]))
        raise ValueError("Invalid nameserver_address")

    def run(self, address_receiver=None, nameserver_address=None):
        '''Run the listener and answer to requests.'''
        if self._server is not None:
            raise RuntimeError("NameServer is already running")

        bind_addr = self._normalize_address(nameserver_address)
        handler_cls = self._make_handler()

        self._server = _ThreadingTCPServer(bind_addr, handler_cls)

        # Report bound address
        bound = self._server.server_address
        if address_receiver is not None:
            try:
                if callable(address_receiver):
                    address_receiver(bound)
                elif hasattr(address_receiver, "put"):
                    address_receiver.put(bound)
                elif hasattr(address_receiver, "send"):
                    address_receiver.send(bound)
            except Exception:
                pass

        self._stopping.clear()
        self._started.set()

        if self.max_age is not None:
            self._cleaner_thread = threading.Thread(
                target=self._cleaner, name="NameServerCleaner", daemon=True)
            self._cleaner_thread.start()

        try:
            self._server.serve_forever(poll_interval=0.5)
        finally:
            try:
                self._server.server_close()
            finally:
                self._server = None
                self._started.clear()
                self._stopping.set()

    def stop(self):
        '''Stop the nameserver.'''
        if self._server is None:
            return
        self._stopping.set()
        try:
            self._server.shutdown()
        except Exception:
            pass
        # Best effort join cleaner
        if self._cleaner_thread and self._cleaner_thread.is_alive():
            self._cleaner_thread.join(timeout=2.0)
        self._cleaner_thread = None
