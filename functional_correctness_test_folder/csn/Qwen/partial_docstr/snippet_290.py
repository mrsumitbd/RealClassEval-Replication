
import zmq
import threading


class ZMQNameServer:
    '''The name server.'''

    def __init__(self):
        self.context = zmq.Context()
        self.socket = None
        self.running = False
        self.thread = None

    def run(self, address_receiver, address: str | None = None):
        '''Run the listener and answer to requests.'''
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(address or "tcp://*:5555")
        self.running = True
        self.thread = threading.Thread(
            target=self._listen, args=(address_receiver,))
        self.thread.start()

    def _listen(self, address_receiver):
        while self.running:
            message = self.socket.recv_string()
            response = address_receiver(message)
            self.socket.send_string(response)

    def close_sockets_and_threads(self):
        if self.socket:
            self.socket.close()
        if self.thread and self.thread.is_alive():
            self.thread.join()

    def stop(self):
        self.running = False
        self.close_sockets_and_threads()
        self.context.term()
