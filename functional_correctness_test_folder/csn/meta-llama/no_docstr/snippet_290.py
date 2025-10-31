
import zmq
import threading
import logging


class ZMQNameServer:

    def __init__(self):
        self.context = zmq.Context()
        self.registry = {}
        self.lock = threading.Lock()
        self.stopped = threading.Event()
        self.receiver_thread = None

    def run(self, address_receiver, address: str | None = None):
        self.receiver_socket = self.context.socket(zmq.REP)
        if address:
            self.receiver_socket.bind(address)
        else:
            self.receiver_socket.bind(address_receiver)

        self.receiver_thread = threading.Thread(
            target=self._receive_requests, args=(address_receiver,))
        self.receiver_thread.start()

    def _receive_requests(self, address_receiver):
        while not self.stopped.is_set():
            try:
                message = self.receiver_socket.recv_json(flags=zmq.NOBLOCK)
                response = self._handle_request(message)
                self.receiver_socket.send_json(response)
            except zmq.Again:
                self.stopped.wait(0.1)
            except Exception as e:
                logging.error(f"Error handling request: {e}")

    def _handle_request(self, message):
        if message['type'] == 'register':
            with self.lock:
                self.registry[message['name']] = message['address']
            return {'status': 'ok'}
        elif message['type'] == 'lookup':
            with self.lock:
                address = self.registry.get(message['name'])
            if address:
                return {'status': 'ok', 'address': address}
            else:
                return {'status': 'not_found'}
        elif message['type'] == 'unregister':
            with self.lock:
                if message['name'] in self.registry:
                    del self.registry[message['name']]
            return {'status': 'ok'}
        else:
            return {'status': 'error', 'message': 'Unknown request type'}

    def close_sockets_and_threads(self):
        if self.receiver_socket:
            self.receiver_socket.close()
        if self.context:
            self.context.term()

    def stop(self):
        self.stopped.set()
        if self.receiver_thread:
            self.receiver_thread.join()
        self.close_sockets_and_threads()
