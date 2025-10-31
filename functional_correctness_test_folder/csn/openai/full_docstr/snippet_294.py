
import threading
import time
import pickle


class ListenerContainer:
    '''Container for a listener instance.'''

    def __init__(self, topics=None, addresses=None, nameserver='localhost', services=''):
        '''Initialize the class.'''
        self.topics = topics or []
        self.addresses = addresses or []
        self.nameserver = nameserver
        self.services = services
        self._stop_event = threading.Event()
        self._thread = None
        self._start_listener()

    def _start_listener(self):
        '''Internal helper to start the listener thread.'''
        if self._thread and self._thread.is_alive():
            self.stop()
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run_listener, daemon=True)
        self._thread.start()

    def _run_listener(self):
        '''Internal listener loop.'''
        # In a real implementation this would connect to a messaging system.
        # Here we just simulate a running listener.
        while not self._stop_event.is_set():
            # Simulate listening work
            time.sleep(0.1)

    def __setstate__(self, state):
        '''Re-initialize the class.'''
        # Restore attributes
        self.__dict__.update(state)
        # Recreate transient attributes
        if not hasattr(self, '_stop_event') or self._stop_event is None:
            self._stop_event = threading.Event()
        if not hasattr(self, '_thread') or self._thread is None:
            self._thread = None
        # Restart listener thread
        self._start_listener()

    def restart_listener(self, topics):
        '''Restart listener after configuration update.'''
        self.topics = topics
        self._start_listener()

    def stop(self):
        '''Stop listener.'''
        if self._thread and self._thread.is_alive():
            self._stop_event.set()
            self._thread.join()
            self._thread = None
