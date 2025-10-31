
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
        self.proxy = ServerProxy(f'http://{nameserver}:9000')
        self._start_listener()

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.proxy = ServerProxy(f'http://{self.nameserver}:9000')
        self._start_listener()

    def _start_listener(self):
        if self.listener is not None:
            self.stop()
        self.listener = threading.Thread(target=self._listen)
        self.listener.daemon = True
        self.listener.start()

    def _listen(self):
        # Assuming some listener logic here
        # For demonstration purposes, just print the topics
        for topic in self.topics:
            print(f'Listening to {topic}')

    def restart_listener(self, topics):
        '''Restart listener after configuration update.'''
        self.topics = topics
        self._start_listener()

    def stop(self):
        if self.listener is not None:
            # Assuming some logic to stop the listener
            # For demonstration purposes, just set the listener to None
            self.listener = None
