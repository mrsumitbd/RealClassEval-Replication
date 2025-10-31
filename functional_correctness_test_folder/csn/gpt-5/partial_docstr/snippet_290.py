import threading
import json
from typing import Callable, Optional, Any
import zmq


class ZMQNameServer:
    '''The name server.'''

    def __init__(self):
        self._ctx: Optional[zmq.Context] = None
        self._sock: Optional[zmq.Socket] = None
        self._stop_event = threading.Event()
        self._running = False
        self._registry: dict[str, str] = {}
        self._thread: Optional[threading.Thread] = None
        self._endpoint: Optional[str] = None

    def _notify_address(self, address_receiver: Any, endpoint: str):
        if address_receiver is None:
            return
        try:
            if callable(address_receiver):
                address_receiver(endpoint)
            elif hasattr(address_receiver, "put") and callable(address_receiver.put):
                address_receiver.put(endpoint)
            elif hasattr(address_receiver, "send") and callable(address_receiver.send):
                address_receiver.send(endpoint)
        except Exception:
            pass

    def _bind_socket(self, address: Optional[str]) -> str:
        self._ctx = zmq.Context.instance()
        self._sock = self._ctx.socket(zmq.REP)
        self._sock.linger = 0
        # Make sure we can periodically check for stop
        self._sock.rcvtimeo = 500  # ms
        if address:
            self._sock.bind(address)
            endpoint = self._sock.getsockopt_string(zmq.LAST_ENDPOINT)
        else:
            # Bind to random port on localhost
            port = self._sock.bind_to_random_port("tcp://127.0.0.1")
            endpoint = f"tcp://127.0.0.1:{port}"
        self._endpoint = endpoint
        return endpoint

    def _handle_message(self, msg: bytes) -> dict:
        try:
            data = json.loads(msg.decode("utf-8"))
        except Exception:
            return {"ok": False, "error": "invalid_json"}

        cmd = data.get("cmd")
        if not isinstance(cmd, str):
            return {"ok": False, "error": "missing_or_invalid_cmd"}

        if cmd == "ping":
            return {"ok": True, "pong": True}

        if cmd == "register":
            name = data.get("name")
            endpoint = data.get("endpoint")
            if not isinstance(name, str) or not isinstance(endpoint, str):
                return {"ok": False, "error": "invalid_name_or_endpoint"}
            self._registry[name] = endpoint
            return {"ok": True}

        if cmd == "lookup":
            name = data.get("name")
            if not isinstance(name, str):
                return {"ok": False, "error": "invalid_name"}
            return {"ok": True, "endpoint": self._registry.get(name)}

        if cmd == "unregister":
            name = data.get("name")
            if not isinstance(name, str):
                return {"ok": False, "error": "invalid_name"}
            existed = name in self._registry
            self._registry.pop(name, None)
            return {"ok": True, "removed": existed}

        if cmd == "list":
            return {"ok": True, "names": list(self._registry.keys())}

        if cmd == "shutdown":
            self._stop_event.set()
            return {"ok": True}

        return {"ok": False, "error": "unknown_cmd"}

    def _serve(self, address_receiver: Any, address: Optional[str]):
        try:
            endpoint = self._bind_socket(address)
        except Exception:
            self._running = False
            return
        self._notify_address(address_receiver, endpoint)

        self._running = True
        try:
            while not self._stop_event.is_set():
                try:
                    msg = self._sock.recv()  # rcvtimeo set
                except zmq.Again:
                    continue
                except Exception:
                    break
                resp = self._handle_message(msg)
                try:
                    self._sock.send(json.dumps(resp).encode("utf-8"))
                except Exception:
                    # If send fails, try to continue
                    pass
        finally:
            self.close_sockets_and_threads()

    def run(self, address_receiver, address: str | None = None):
        '''Run the listener and answer to requests.'''
        if self._running:
            return
        self._stop_event.clear()
        # Run in the current thread, blocking
        self._serve(address_receiver, address)

    def close_sockets_and_threads(self):
        if self._sock is not None:
            try:
                self._sock.close(0)
            except Exception:
                pass
            self._sock = None
        if self._ctx is not None:
            try:
                # Do not terminate the shared instance for safety; close if ours
                # Using instance() above, so don't call terminate to avoid impacting others.
                pass
            except Exception:
                pass
            self._ctx = None
        self._running = False

    def stop(self):
        self._stop_event.set()
