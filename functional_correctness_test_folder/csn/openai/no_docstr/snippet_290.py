
import json
import threading
import zmq
import time
from typing import Optional, Dict, Any


class ZMQNameServer:
    """
    A simple ZeroMQ-based name server.

    The server exposes a REP socket that accepts JSON messages with the following
    structure:

        {"action": "register", "name": "<name>", "address": "<address>"}
        {"action": "lookup",   "name": "<name>"}
        {"action": "unregister","name": "<name>"}
        {"action": "list"}

    The server maintains an in‑memory dictionary mapping names to addresses.
    """

    def __init__(self):
        # ZeroMQ context
        self._ctx = zmq.Context.instance()

        # Sockets (created in run)
        self._rep_socket: Optional[zmq.Socket] = None
        self._pub_socket: Optional[zmq.Socket] = None

        # Thread that runs the event loop
        self._thread: Optional[threading.Thread] = None

        # Flag to stop the server
        self._stop_event = threading.Event()

        # In‑memory registry
        self._registry: Dict[str, str] = {}

        # Lock for registry access
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def run(self, address_receiver: str, address: Optional[str] = None) -> None:
        """
        Start the name server.

        Parameters
        ----------
        address_receiver : str
            The address to bind the REP socket (e.g. "tcp://*:5555").
        address : Optional[str]
            If provided, a PUB socket will be bound to this address to
            broadcast registration events.
        """
        if self._thread and self._thread.is_alive():
            raise RuntimeError("Server is already running")

        # Create REP socket
        self._rep_socket = self._ctx.socket(zmq.REP)
        self._rep_socket.bind(address_receiver)

        # Optional PUB socket
        if address:
            self._pub_socket = self._ctx.socket(zmq.PUB)
            self._pub_socket.bind(address)

        # Start the worker thread
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._serve, daemon=True)
        self._thread.start()

    def close_sockets_and_threads(self) -> None:
        """
        Close all sockets and wait for the worker thread to finish.
        """
        self.stop()
        if self._thread:
            self._thread.join()
            self._thread = None

        if self._rep_socket:
            try:
                self._rep_socket.close(0)
            except Exception:
                pass
            self._rep_socket = None

        if self._pub_socket:
            try:
                self._pub_socket.close(0)
            except Exception:
                pass
            self._pub_socket = None

        # Terminate the context only if no other sockets are using it
        try:
            self._ctx.term()
        except Exception:
            pass

    def stop(self) -> None:
        """
        Signal the server to stop.
        """
        self._stop_event.set()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _serve(self) -> None:
        """
        Main loop that processes incoming requests.
        """
        while not self._stop_event.is_set():
            try:
                # Use a short poll timeout to allow graceful shutdown
                socks = dict(self._rep_socket.poll(100, zmq.POLLIN))
                if socks.get(self._rep_socket) == zmq.POLLIN:
                    msg = self._rep_socket.recv_string(zmq.NOBLOCK)
                    response = self._handle_request(msg)
                    self._rep_socket.send_string(response)
            except zmq.Again:
                # No message received
                continue
            except Exception as exc:
                # Log the error and send a generic error response
                error_resp = json.dumps(
                    {"status": "error", "message": str(exc)})
                try:
                    self._rep_socket.send_string(error_resp)
                except Exception:
                    pass
                continue

    def _handle_request(self, msg: str) -> str:
        """
        Parse the incoming JSON message and perform the requested action.
        """
        try:
            data = json.loads(msg)
        except json.JSONDecodeError:
            return json.dumps({"status": "error", "message": "Invalid JSON"})

        action = data.get("action")
        if not action:
            return json.dumps({"status": "error", "message": "Missing action"})

        if action == "register":
            return self._register(data)
        elif action == "lookup":
            return self._lookup(data)
        elif action == "unregister":
            return self._unregister(data)
        elif action == "list":
            return self._list()
        else:
            return json.dumps({"status": "error", "message": f"Unknown action '{action}'"})

    def _register(self, data: Dict[str, Any]) -> str:
        name = data.get("name")
        address = data.get("address")
        if not name or not address:
            return json.dumps({"status": "error", "message": "Missing name or address"})

        with self._lock:
            self._registry[name] = address

        # Broadcast the registration if PUB socket is available
        if self._pub_socket:
            try:
                self._pub_socket.send_string(json.dumps(
                    {"event": "register", "name": name, "address": address}))
            except Exception:
                pass

        return json.dumps({"status": "ok", "message": f"Registered {name}"})

    def _lookup(self, data: Dict[str, Any]) -> str:
        name = data.get("name")
        if not name:
            return json.dumps({"status": "error", "message": "Missing name"})

        with self._lock:
            address = self._registry.get(name)

        if address:
            return json.dumps({"status": "ok", "address": address})
        else:
            return json.dumps({"status": "error", "message": f"Name '{name}' not found"})

    def _unregister(self, data: Dict[str, Any]) -> str:
        name = data.get("name")
        if not name:
            return json.dumps({"status": "error", "message": "Missing name"})

        with self._lock:
            removed = self._registry.pop(name, None)

        if removed:
            if self._pub_socket:
                try:
                    self._pub_socket.send_string(json.dumps(
                        {"event": "unregister", "name": name}))
                except Exception:
                    pass
            return json.dumps({"status": "ok", "message": f"Unregistered {name}"})
        else:
            return json.dumps({"status": "error", "message": f"Name '{name}' not found"})

    def _list(self) -> str:
        with self._lock:
            names = list(self._registry.keys())
        return json.dumps({"status": "ok", "names": names})
