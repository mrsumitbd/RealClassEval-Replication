
import json
import threading
import time
from typing import Optional

import zmq


class ZMQNameServer:
    '''The name server.'''

    def __init__(self):
        '''Set up the nameserver.'''
        self._context = zmq.Context.instance()
        self._socket: Optional[zmq.Socket] = None
        self._thread: Optional[threading.Thread] = None
        self._running = False
        self._registry = {}  # name -> address

    def run(self, address_receiver: str, address: str | None = None):
        '''Run the listener and answer to requests.'''
        if self._running:
            raise RuntimeError("Name server already running")

        # Create a REP socket for request/response
        self._socket = self._context.socket(zmq.REP)
        self._socket.bind(address_receiver)

        # If an address is provided, register it under a default name
        if address is not None:
            self._registry["default"] = address

        self._running = True

        def _serve():
            poller = zmq.Poller()
            poller.register(self._socket, zmq.POLLIN)
            while self._running:
                socks = dict(poller.poll(100))
                if self._socket in socks and socks[self._socket] == zmq.POLLIN:
                    try:
                        msg = self._socket.recv_string(flags=zmq.NOBLOCK)
                    except zmq.Again:
                        continue
                    try:
                        data = json.loads(msg)
                    except json.JSONDecodeError:
                        # Malformed request; reply with error
                        reply = {"status": "error", "reason": "invalid json"}
                        self._socket.send_string(json.dumps(reply))
                        continue

                    action = data.get("action")
                    if action == "register":
                        name = data.get("name")
                        addr = data.get("address")
                        if name and addr:
                            self._registry[name] = addr
                            reply = {"status": "ok", "registered": name}
                        else:
                            reply = {"status": "error",
                                     "reason": "missing name or address"}
                    elif action == "query":
                        name = data.get("name")
                        if name:
                            addr = self._registry.get(name)
                            if addr:
                                reply = {"status": "ok", "address": addr}
                            else:
                                reply = {"status": "error",
                                         "reason": "name not found"}
                        else:
                            reply = {"status": "error",
                                     "reason": "missing name"}
                    else:
                        reply = {"status": "error", "reason": "unknown action"}

                    self._socket.send_string(json.dumps(reply))
                else:
                    # No message; sleep briefly to avoid busy loop
                    time.sleep(0.01)

        self._thread = threading.Thread(target=_serve, daemon=True)
        self._thread.start()

    def close_sockets_and_threads(self):
        '''Close all sockets and threads.'''
        self.stop()
        if self._socket:
            try:
                self._socket.close(0)
            except Exception:
                pass
            self._socket = None
        if self._thread:
            self._thread.join(timeout=1.0)
            self._thread = None
        # Note: we do not terminate the context here to allow reuse

    def stop(self):
        '''Stop the name server.'''
        self._running = False
