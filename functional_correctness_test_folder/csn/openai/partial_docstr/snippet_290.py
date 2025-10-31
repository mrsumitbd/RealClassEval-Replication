
import json
import threading
import zmq
from typing import Optional, Dict


class ZMQNameServer:
    '''The name server.'''

    def __init__(self):
        # ZeroMQ context and sockets will be created in run()
        self._context: Optional[zmq.Context] = None
        self._socket: Optional[zmq.Socket] = None
        self._thread: Optional[threading.Thread] = None
        self._running = False
        # Simple registry: service name -> address
        self._registry: Dict[str, str] = {}

    def run(self, address_receiver: str, address: str | None = None):
        '''Run the listener and answer to requests.'''
        if self._running:
            raise RuntimeError("Name server already running")

        self._context = zmq.Context.instance()
        self._socket = self._context.socket(zmq.REP)
        self._socket.bind(address_receiver)

        # If an address is provided, register it under a default key
        if address is not None:
            self._registry["default"] = address

        self._running = True

        def _serve():
            poller = zmq.Poller()
            poller.register(self._socket, zmq.POLLIN)
            while self._running:
                socks = dict(poller.poll(1000))
                if self._socket in socks and socks[self._socket] == zmq.POLLIN:
                    try:
                        msg = self._socket.recv_string(flags=zmq.NOBLOCK)
                    except zmq.Again:
                        continue
                    try:
                        request = json.loads(msg)
                        service = request.get("service")
                        if service in self._registry:
                            reply = {"address": self._registry[service]}
                        else:
                            reply = {"error": f"service '{service}' not found"}
                    except Exception as exc:
                        reply = {"error": str(exc)}
                    self._socket.send_string(json.dumps(reply))
            # Clean up socket when loop exits
            self._socket.close(0)

        self._thread = threading.Thread(target=_serve, daemon=True)
        self._thread.start()

    def close_sockets_and_threads(self):
        '''Close sockets and join the server thread.'''
        self.stop()
        if self._thread is not None:
            self._thread.join()
            self._thread = None
        if self._socket is not None:
            self._socket.close(0)
            self._socket = None
        if self._context is not None:
            self._context.term()
            self._context = None

    def stop(self):
        '''Signal the server thread to stop.'''
        self._running = False
