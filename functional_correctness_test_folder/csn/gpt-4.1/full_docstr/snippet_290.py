
import threading
import zmq
import time


class ZMQNameServer:
    '''The name server.'''

    def __init__(self):
        '''Set up the nameserver.'''
        self.context = zmq.Context()
        self.socket = None
        self.running = False
        self.thread = None
        self.address_receiver = None
        self.address = None
        self.lock = threading.Lock()

    def _listener(self):
        while self.running:
            try:
                if self.socket.poll(100):  # 100 ms timeout
                    msg = self.socket.recv_json(zmq.NOBLOCK)
                    # address_receiver is a callable that returns a dict or str
                    if callable(self.address_receiver):
                        response = self.address_receiver(msg)
                    else:
                        response = {}
                    self.socket.send_json(response)
                else:
                    time.sleep(0.01)
            except zmq.ZMQError as e:
                if not self.running:
                    break
                continue
            except Exception:
                continue

    def run(self, address_receiver, address: str | None = None):
        '''Run the listener and answer to requests.'''
        with self.lock:
            if self.running:
                return
            self.address_receiver = address_receiver
            self.address = address or "tcp://127.0.0.1:5555"
            self.socket = self.context.socket(zmq.REP)
            self.socket.bind(self.address)
            self.running = True
            self.thread = threading.Thread(target=self._listener, daemon=True)
            self.thread.start()

    def close_sockets_and_threads(self):
        '''Close all sockets and threads.'''
        with self.lock:
            self.running = False
            if self.thread is not None:
                self.thread.join(timeout=1)
                self.thread = None
            if self.socket is not None:
                try:
                    self.socket.close(0)
                except Exception:
                    pass
                self.socket = None
            if self.context is not None:
                try:
                    self.context.term()
                except Exception:
                    pass
                self.context = None

    def stop(self):
        '''Stop the name server.'''
        self.close_sockets_and_threads()
