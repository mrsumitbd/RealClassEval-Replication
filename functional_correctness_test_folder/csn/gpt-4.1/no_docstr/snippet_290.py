
import threading
import zmq
import time


class ZMQNameServer:

    def __init__(self):
        self.context = zmq.Context()
        self.receiver_socket = None
        self.publisher_socket = None
        self.running = False
        self.receiver_thread = None
        self.address = None
        self.address_receiver = None

    def run(self, address_receiver, address: str | None = None):
        self.address_receiver = address_receiver
        self.address = address or "tcp://*:5555"
        self.receiver_socket = self.context.socket(zmq.REP)
        self.receiver_socket.bind(self.address)
        self.running = True
        self.receiver_thread = threading.Thread(
            target=self._receiver_loop, daemon=True)
        self.receiver_thread.start()

    def _receiver_loop(self):
        while self.running:
            try:
                if self.receiver_socket.poll(100, zmq.POLLIN):
                    msg = self.receiver_socket.recv_string()
                    response = self.address_receiver(msg)
                    self.receiver_socket.send_string(str(response))
                else:
                    time.sleep(0.01)
            except zmq.ZMQError:
                break
            except Exception:
                self.receiver_socket.send_string("ERROR")

    def close_sockets_and_threads(self):
        self.running = False
        if self.receiver_thread and self.receiver_thread.is_alive():
            self.receiver_thread.join(timeout=1)
        if self.receiver_socket:
            self.receiver_socket.close(0)
            self.receiver_socket = None
        if self.context:
            self.context.term()
            self.context = None

    def stop(self):
        self.close_sockets_and_threads()
