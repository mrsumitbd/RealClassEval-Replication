import threading
import json
import time
from typing import Optional
try:
    import zmq
except ImportError as e:
    raise ImportError(
        "pyzmq is required to use ZMQNameServer. Install with: pip install pyzmq") from e


class ZMQNameServer:
    def __init__(self):
        self._context = zmq.Context.instance()
        self._sub_sock = None
        self._rep_sock = None
        self._recv_thread = None
        self._serve_thread = None
        self._stop_event = threading.Event()
        self._registry = {}
        self._lock = threading.RLock()

    def run(self, address_receiver, address: str | None = None):
        if self._recv_thread or self._serve_thread:
            return

        if address is None:
            address = "tcp://*:5555"

        self._sub_sock = self._context.socket(zmq.SUB)
        self._sub_sock.setsockopt(zmq.SUBSCRIBE, b"")
        self._sub_sock.connect(address_receiver)

        self._rep_sock = self._context.socket(zmq.REP)
        self._rep_sock.bind(address)

        self._stop_event.clear()
        self._recv_thread = threading.Thread(
            target=self._recv_loop, name="ZMQNameServer-Receiver", daemon=True)
        self._serve_thread = threading.Thread(
            target=self._serve_loop, name="ZMQNameServer-Server", daemon=True)
        self._recv_thread.start()
        self._serve_thread.start()

    def close_sockets_and_threads(self):
        self._stop_event.set()

        try:
            if self._sub_sock is not None:
                self._sub_sock.close(linger=0)
        except Exception:
            pass
        finally:
            self._sub_sock = None

        try:
            if self._rep_sock is not None:
                self._rep_sock.close(linger=0)
        except Exception:
            pass
        finally:
            self._rep_sock = None

        if self._recv_thread is not None:
            self._recv_thread.join(timeout=2.0)
            self._recv_thread = None

        if self._serve_thread is not None:
            self._serve_thread.join(timeout=2.0)
            self._serve_thread = None

        try:
            # Do not terminate the shared instance context if other users might rely on it.
            # But if no sockets are open, terminating is fine.
            self._context.term()
        except Exception:
            pass

    def stop(self):
        self.close_sockets_and_threads()

    # Internal methods

    def _recv_loop(self):
        poller = zmq.Poller()
        if self._sub_sock is None:
            return
        poller.register(self._sub_sock, zmq.POLLIN)

        while not self._stop_event.is_set():
            try:
                events = dict(poller.poll(timeout=200))
            except zmq.error.ZMQError:
                break

            if self._sub_sock in events and events[self._sub_sock] & zmq.POLLIN:
                try:
                    msg = self._sub_sock.recv_string(flags=zmq.NOBLOCK).strip()
                except zmq.Again:
                    continue
                except Exception:
                    continue
                self._handle_announcement(msg)

        # Drain
        try:
            poller.unregister(self._sub_sock)
        except Exception:
            pass

    def _serve_loop(self):
        poller = zmq.Poller()
        if self._rep_sock is None:
            return
        poller.register(self._rep_sock, zmq.POLLIN)

        while not self._stop_event.is_set():
            try:
                events = dict(poller.poll(timeout=200))
            except zmq.error.ZMQError:
                break

            if self._rep_sock in events and events[self._rep_sock] & zmq.POLLIN:
                try:
                    req = self._rep_sock.recv_string().strip()
                except Exception:
                    # If something went wrong, try to send a generic error
                    self._safe_send_rep("ERR")
                    continue
                resp = self._handle_request(req)
                self._safe_send_rep(resp)

        try:
            poller.unregister(self._rep_sock)
        except Exception:
            pass

    def _safe_send_rep(self, msg: str):
        try:
            if self._rep_sock is not None:
                self._rep_sock.send_string(msg)
        except Exception:
            pass

    def _handle_announcement(self, msg: str):
        parts = msg.split()
        if not parts:
            return
        cmd = parts[0].upper()

        if cmd == "REGISTER" and len(parts) >= 3:
            name = parts[1]
            addr = " ".join(parts[2:])
            with self._lock:
                self._registry[name] = addr
        elif cmd == "UNREGISTER" and len(parts) >= 2:
            name = parts[1]
            with self._lock:
                self._registry.pop(name, None)

    def _handle_request(self, req: str) -> str:
        parts = req.split()
        if not parts:
            return "ERR empty"

        cmd = parts[0].upper()

        if cmd == "PING":
            return "PONG"

        if cmd == "RESOLVE" and len(parts) >= 2:
            name = parts[1]
            with self._lock:
                addr = self._registry.get(name)
            if addr is None:
                return "NOT_FOUND"
            return f"OK {addr}"

        if cmd == "REGISTER" and len(parts) >= 3:
            name = parts[1]
            addr = " ".join(parts[2:])
            with self._lock:
                self._registry[name] = addr
            return "OK"

        if cmd == "UNREGISTER" and len(parts) >= 2:
            name = parts[1]
            with self._lock:
                existed = name in self._registry
                self._registry.pop(name, None)
            return "OK" if existed else "NOT_FOUND"

        if cmd == "LIST":
            with self._lock:
                data = json.dumps(self._registry, separators=(",", ":"))
            return f"OK {data}"

        if cmd == "COUNT":
            with self._lock:
                count = len(self._registry)
            return f"OK {count}"

        return "ERR unknown_command"
