
import threading
import zmq
from typing import Optional


class ZMQNameServer:
    '''The name server.'''

    def __init__(self):
        '''Set up the nameserver.'''
        self.context = zmq.Context()
        self.receiver_socket = None
        self.publisher_socket = None
        self.running = False
        self.thread = None

    def run(self, address_receiver, address: Optional[str] = None):
        '''Run the listener and answer to requests.'''
        if self.running:
            return

        self.running = True
        self.receiver_socket = self.context.socket(zmq.REP)
        self.receiver_socket.bind(address_receiver)

        if address is not None:
            self.publisher_socket = self.context.socket(zmq.PUB)
            self.publisher_socket.bind(address)

        def listener():
            while self.running:
                try:
                    message = self.receiver_socket.recv_json(flags=zmq.NOBLOCK)
                    if message.get('command') == 'stop':
                        self.stop()
                        break
                    # Handle other commands here
                    self.receiver_socket.send_json({'status': 'ok'})
                except zmq.Again:
                    continue
                except Exception as e:
                    print(f"Error handling request: {e}")
                    self.receiver_socket.send_json(
                        {'status': 'error', 'message': str(e)})

        self.thread = threading.Thread(target=listener)
        self.thread.start()

    def close_sockets_and_threads(self):
        '''Close all sockets and threads.'''
        if self.receiver_socket:
            self.receiver_socket.close()
        if self.publisher_socket:
            self.publisher_socket.close()
        if self.thread and self.thread.is_alive():
            self.thread.join()

    def stop(self):
        '''Stop the name server.'''
        self.running = False
        self.close_sockets_and_threads()
