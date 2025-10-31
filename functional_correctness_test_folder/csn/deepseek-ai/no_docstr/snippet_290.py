
import threading
import zmq


class ZMQNameServer:

    def __init__(self):
        self.context = zmq.Context()
        self.receiver_socket = None
        self.publisher_socket = None
        self.running = False
        self.thread = None

    def run(self, address_receiver, address: str | None = None):
        if self.running:
            return

        self.running = True
        self.receiver_socket = self.context.socket(zmq.REP)
        self.receiver_socket.bind(address_receiver)

        if address is not None:
            self.publisher_socket = self.context.socket(zmq.PUB)
            self.publisher_socket.bind(address)

        self.thread = threading.Thread(target=self._run_loop)
        self.thread.start()

    def _run_loop(self):
        while self.running:
            try:
                message = self.receiver_socket.recv_json(flags=zmq.NOBLOCK)
                if message.get("command") == "stop":
                    self.stop()
                    break
                # Handle other commands here
                self.receiver_socket.send_json({"status": "ok"})
            except zmq.Again:
                continue

    def close_sockets_and_threads(self):
        if self.receiver_socket:
            self.receiver_socket.close()
        if self.publisher_socket:
            self.publisher_socket.close()
        if self.thread and self.thread.is_alive():
            self.thread.join()

    def stop(self):
        self.running = False
        self.close_sockets_and_threads()
