
import threading
import zmq
import time


class ZMQNameServer:
    '''The name server.'''

    def __init__(self):
        self.context = zmq.Context()
        self.socket = None
        self.running = False
        self.thread = None
        self.addresses = {}
        self._lock = threading.Lock()

    def run(self, address_receiver, address: str | None = None):
        '''Run the listener and answer to requests.'''
        if self.running:
            return
        self.running = True
        self.socket = self.context.socket(zmq.REP)
        bind_addr = address if address is not None else "tcp://127.0.0.1:5555"
        self.socket.bind(bind_addr)

        def listen():
            while self.running:
                try:
                    if self.socket.poll(100, zmq.POLLIN):
                        msg = self.socket.recv_json()
                        cmd = msg.get("cmd")
                        if cmd == "register":
                            name = msg.get("name")
                            addr = msg.get("address")
                            with self._lock:
                                self.addresses[name] = addr
                            self.socket.send_json({"status": "ok"})
                        elif cmd == "lookup":
                            name = msg.get("name")
                            with self._lock:
                                addr = self.addresses.get(name)
                            if addr is not None:
                                self.socket.send_json(
                                    {"status": "ok", "address": addr})
                            else:
                                self.socket.send_json({"status": "not_found"})
                        elif cmd == "list":
                            with self._lock:
                                names = list(self.addresses.keys())
                            self.socket.send_json(
                                {"status": "ok", "names": names})
                        elif cmd == "unregister":
                            name = msg.get("name")
                            with self._lock:
                                if name in self.addresses:
                                    del self.addresses[name]
                                    self.socket.send_json({"status": "ok"})
                                else:
                                    self.socket.send_json(
                                        {"status": "not_found"})
                        elif cmd == "stop":
                            self.socket.send_json({"status": "stopping"})
                            self.running = False
                        else:
                            self.socket.send_json(
                                {"status": "error", "error": "unknown command"})
                    else:
                        time.sleep(0.01)
                except zmq.ZMQError:
                    break
                except Exception:
                    try:
                        self.socket.send_json(
                            {"status": "error", "error": "exception"})
                    except Exception:
                        pass
            self.socket.close(0)

        self.thread = threading.Thread(target=listen, daemon=True)
        self.thread.start()

    def close_sockets_and_threads(self):
        self.running = False
        if self.socket is not None:
            try:
                self.socket.close(0)
            except Exception:
                pass
            self.socket = None
        if self.thread is not None:
            self.thread.join(timeout=1)
            self.thread = None
        if self.context is not None:
            try:
                self.context.term()
            except Exception:
                pass
            self.context = None

    def stop(self):
        self.running = False
        if self.socket is not None:
            try:
                # Send a dummy stop message to unblock the socket if needed
                dummy_context = zmq.Context()
                dummy_socket = dummy_context.socket(zmq.REQ)
                try:
                    dummy_socket.connect(self.socket.LAST_ENDPOINT)
                    dummy_socket.send_json({"cmd": "stop"})
                    dummy_socket.recv_json()
                except Exception:
                    pass
                dummy_socket.close(0)
                dummy_context.term()
            except Exception:
                pass
        self.close_sockets_and_threads()
