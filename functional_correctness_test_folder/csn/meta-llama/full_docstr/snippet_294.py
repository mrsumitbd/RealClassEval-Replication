
import threading
from xmlrpc.client import ServerProxy


class ListenerContainer:
    '''Container for a listener instance.'''

    def __init__(self, topics=None, addresses=None, nameserver='localhost', services=''):
        '''Initialize the class.'''
        self.topics = topics if topics is not None else []
        self.addresses = addresses if addresses is not None else []
        self.nameserver = nameserver
        self.services = services
        self.listener = None
        self.proxy = ServerProxy(f'http://{nameserver}:8080')
        self._start_listener()

    def __setstate__(self, state):
        '''Re-initialize the class.'''
        self.__dict__.update(state)
        self.proxy = ServerProxy(f'http://{self.nameserver}:8080')
        self._start_listener()

    def _start_listener(self):
        '''Start the listener.'''
        if self.listener is None or not self.listener.is_alive():
            self.listener = threading.Thread(target=self._listen)
            self.listener.daemon = True
            self.listener.start()

    def _listen(self):
        '''Listen to the specified topics.'''
        # Simulating listener functionality
        while True:
            for topic in self.topics:
                # Replace this with actual listener logic
                print(f'Listening to {topic}')

    def restart_listener(self, topics):
        '''Restart listener after configuration update.'''
        self.topics = topics
        self.stop()
        self._start_listener()

    def stop(self):
        '''Stop listener.'''
        if self.listener is not None:
            # Since we're using a daemon thread, it will exit when the main program exits
            # For a more complex listener, you might need to implement a way to stop it
            self.listener = None
