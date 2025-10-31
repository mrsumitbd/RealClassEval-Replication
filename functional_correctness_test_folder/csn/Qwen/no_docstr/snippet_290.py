
import zmq
import threading


class ZMQNameServer:

    def __init__(self):
        self.context = zmq.Context()
        self.receiver = None
        self.poller = zmq.Poller()
        self.running = False
        self.threads = []

    def run(self, address_receiver, address: str | None = None):
        self.receiver = self.context.socket(zmq.PULL)
        self.receiver.bind(address_receiver)
        self.poller.register(self.receiver, zmq.POLLIN)
        self.running = True

        if address:
            self.sender = self.context.socket(zmq.PUSH)
            self.sender.bind(address)
        else:
            self.sender = None

        thread = threading.Thread(target=self._process_messages)
        thread.start()
        self.threads.append(thread)

    def _process_messages(self):
        while self.running:
            socks = dict(self.poller.poll(1000))
            if self.receiver in socks and socks[self.receiver] == zmq.POLLIN:
                message = self.receiver.recv_json()
                if self.sender:
                    self.sender.send_json(message)

    def close_sockets_and_threads(self):
        if self.receiver:
            self.poller.unregister(self.receiver)
            self.receiver.close()
        if self.sender:
            self.sender.close()
        self.context.term()

    def stop(self):
        self.running = False
        for thread in self.threads:
            thread.join()
        self.close_sockets_and_threads()
