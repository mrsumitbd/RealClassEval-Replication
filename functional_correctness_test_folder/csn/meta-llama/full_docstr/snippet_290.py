
import zmq
import threading


class ZMQNameServer:
    '''The name server.'''

    def __init__(self):
        '''Set up the nameserver.'''
        self.context = zmq.Context()
        self.names = {}
        self.lock = threading.Lock()
        self.stopped = threading.Event()

    def run(self, address_receiver, address: str | None = None):
        '''Run the listener and answer to requests.'''
        self.socket = self.context.socket(zmq.REP)
        if address is not None:
            self.socket.bind(address)
        else:
            port = self.socket.bind_to_random_port(address_receiver)
            print(f"Bound to port {port}")

        self.thread = threading.Thread(target=self._listen)
        self.thread.start()

    def _listen(self):
        while not self.stopped.is_set():
            try:
                message = self.socket.recv(zmq.NOBLOCK)
                response = self._handle_message(message)
                self.socket.send(response)
            except zmq.Again:
                self.stopped.wait(0.1)

    def _handle_message(self, message):
        parts = message.decode().split()
        if parts[0] == "register":
            with self.lock:
                self.names[parts[1]] = parts[2]
            return b"OK"
        elif parts[0] == "lookup":
            with self.lock:
                return self.names.get(parts[1], "").encode()
        elif parts[0] == "unregister":
            with self.lock:
                if parts[1] in self.names:
                    del self.names[parts[1]]
            return b"OK"
        else:
            return b"Unknown command"

    def close_sockets_and_threads(self):
        '''Close all sockets and threads.'''
        self.stopped.set()
        if hasattr(self, 'thread'):
            self.thread.join()
        if hasattr(self, 'socket'):
            self.socket.close()
        self.context.term()

    def stop(self):
        '''Stop the name server.'''
        self.close_sockets_and_threads()
