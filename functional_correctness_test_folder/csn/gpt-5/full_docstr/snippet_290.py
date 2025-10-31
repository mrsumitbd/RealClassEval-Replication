import threading
import json
import time
from typing import Optional

try:
    import zmq
except ImportError:  # Fallback no-op shim to avoid NameError if zmq is absent
    # This shim will raise informative errors upon attempted use.
    class _ZMQShim:
        def __getattr__(self, item):
            raise ImportError("pyzmq is required to use ZMQNameServer")
    zmq = _ZMQShim()


class ZMQNameServer:
    '''The name server.'''

    def __init__(self):
        '''Set up the nameserver.'''
        self._context: Optional["zmq.Context"] = None
        self._rep_socket: Optional["zmq.Socket"] = None
        self._pub_socket: Optional["zmq.Socket"] = None
        self._pub_enabled: bool = False
        self._thread: Optional[threading.Thread] = None
        self._running = threading.Event()
        self._lock = threading.RLock()
        self._registry: dict[str, str] = {}
        self._poll_timeout_ms = 200

    def _ensure_context(self):
        if self._context is None:
            self._context = zmq.Context.instance()

    def _handle_request(self, msg: bytes) -> dict:
        try:
            req = json.loads(msg.decode("utf-8"))
        except Exception:
            return {"status": "error", "error": "invalid_json"}

        if not isinstance(req, dict) or "cmd" not in req:
            return {"status": "error", "error": "invalid_request"}

        cmd = str(req.get("cmd", "")).upper()

        if cmd == "PING":
            return {"status": "ok", "data": "pong"}

        if cmd == "SHUTDOWN":
            self.stop()
            return {"status": "ok", "data": "shutting_down"}

        if cmd == "REGISTER":
            name = req.get("name")
            endpoint = req.get("endpoint")
            if not isinstance(name, str) or not isinstance(endpoint, str):
                return {"status": "error", "error": "missing_or_invalid_name_or_endpoint"}
            with self._lock:
                self._registry[name] = endpoint
            self._publish(
                {"event": "registered", "name": name, "endpoint": endpoint})
            return {"status": "ok"}

        if cmd == "UNREGISTER":
            name = req.get("name")
            if not isinstance(name, str):
                return {"status": "error", "error": "missing_or_invalid_name"}
            with self._lock:
                existed = name in self._registry
                endpoint = self._registry.pop(name, None)
            if existed:
                self._publish({"event": "unregistered",
                              "name": name, "endpoint": endpoint})
                return {"status": "ok"}
            return {"status": "error", "error": "not_found"}

        if cmd == "LOOKUP":
            name = req.get("name")
            if not isinstance(name, str):
                return {"status": "error", "error": "missing_or_invalid_name"}
            with self._lock:
                endpoint = self._registry.get(name)
            if endpoint is None:
                return {"status": "error", "error": "not_found"}
            return {"status": "ok", "endpoint": endpoint}

        if cmd == "LIST":
            with self._lock:
                items = dict(self._registry)
            return {"status": "ok", "items": items}

        return {"status": "error", "error": "unknown_command"}

    def _publish(self, payload: dict):
        if not self._pub_enabled or self._pub_socket is None:
            return
        try:
            self._pub_socket.send_json(payload, flags=zmq.NOBLOCK)
        except Exception:
            pass

    def _loop(self):
        poller = zmq.Poller()
        poller.register(self._rep_socket, zmq.POLLIN)
        while self._running.is_set():
            try:
                events = dict(poller.poll(self._poll_timeout_ms))
            except Exception:
                break
            if self._rep_socket in events and events[self._rep_socket] & zmq.POLLIN:
                try:
                    msg = self._rep_socket.recv(flags=0)
                    resp = self._handle_request(msg)
                    self._rep_socket.send(json.dumps(resp).encode("utf-8"))
                except zmq.ZMQError:
                    break
                except Exception:
                    try:
                        self._rep_socket.send(json.dumps(
                            {"status": "error", "error": "internal"}).encode("utf-8"))
                    except Exception:
                        pass
        # drain and close handled by close_sockets_and_threads

    def run(self, address_receiver, address: str | None = None):
        '''Run the listener and answer to requests.'''
        if self._thread is not None and self._thread.is_alive():
            return
        self._ensure_context()

        self._rep_socket = self._context.socket(zmq.REP)
        self._rep_socket.linger = 0
        self._rep_socket.bind(str(address_receiver))

        if address is not None:
            self._pub_socket = self._context.socket(zmq.PUB)
            self._pub_socket.linger = 0
            self._pub_socket.bind(str(address))
            self._pub_enabled = True
        else:
            self._pub_enabled = False

        self._running.set()
        self._thread = threading.Thread(
            target=self._loop, name="ZMQNameServer", daemon=True)
        self._thread.start()

    def close_sockets_and_threads(self):
        '''Close all sockets and threads.'''
        self._running.clear()
        th = self._thread
        self._thread = None

        if th is not None and th.is_alive():
            th.join(timeout=2.0)

        try:
            if self._rep_socket is not None:
                self._rep_socket.close(0)
        finally:
            self._rep_socket = None

        try:
            if self._pub_socket is not None:
                self._pub_socket.close(0)
        finally:
            self._pub_socket = None

        ctx = self._context
        self._context = None
        if ctx is not None:
            try:
                ctx.term()
            except Exception:
                pass

    def stop(self):
        '''Stop the name server.'''
        self._running.clear()
        # Attempt to poke the loop if it's blocked on poll
        if self._rep_socket is not None:
            try:
                tmp = self._context.socket(zmq.REQ)
                tmp.linger = 0
                # If bound to tcp://*:PORT we can try connecting via localhost.
                # For inproc or ipc, connection attempts will be no-ops if not applicable.
                endpoint = None
                try:
                    # Obtain last endpoint if available (best effort)
                    endpoint = self._rep_socket.getsockopt_string(
                        zmq.LAST_ENDPOINT)
                except Exception:
                    pass
                if endpoint:
                    tmp.connect(endpoint.replace("*", "127.0.0.1"))
                    tmp.send(json.dumps({"cmd": "PING"}).encode("utf-8"))
                    try:
                        tmp.recv(flags=0)
                    except Exception:
                        pass
                tmp.close(0)
            except Exception:
                pass
        self.close_sockets_and_threads()
