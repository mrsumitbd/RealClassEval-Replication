
import threading
import zmq


class ZMQNameServer:
    '''The name server.'''

    def __init__(self):
        self.context = zmq.Context()
        self.socket = None
        self.running = False
        self.thread = None
        self.address = None

    def run(self, address_receiver, address: str | None = None):
        '''Run the listener and answer to requests.'''
        if self.running:
            return

        self.address = address if address is not None else "tcp://*:5555"
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(self.address)

        if address_receiver is not None:
            address_receiver(self.address)

        self.running = True
        self.thread = threading.Thread(target=self._listen)
        self.thread.start()

    def _listen(self):
        while self.running:
            try:
                message = self.socket.recv_string(flags=zmq.NOBLOCK)
                self.socket.send_string("ACK")
            except zmq.Again:
                continue
            except zmq.ZMQError:
                break

    def close_sockets_and_threads(self):
        if not self.running:
            return

        self.running = False
        if self.thread is not None:
            self.thread.join()
            self.thread = None

        if self.socket is not None:
            self.socket.close()
            self.socket = None

    def stop(self):
        self.close_sockets_and_threads()
