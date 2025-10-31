from threading import Thread
from queue import Queue
import logging

class ListenerContainer:
    """Container for a listener instance."""
    logger = logging.getLogger(__name__ + '.ListenerContainer')

    def __init__(self, topics=None, addresses=None, nameserver='localhost', services=''):
        """Initialize the class."""
        self.listener = None
        self.output_queue = None
        self.thread = None
        self.addresses = addresses
        self.nameserver = nameserver
        if topics is not None:
            self.output_queue = Queue()
            self.listener = Listener(topics=topics, queue=self.output_queue, addresses=self.addresses, nameserver=self.nameserver, services=services)
            self.thread = Thread(target=self.listener.run, daemon=True)
            self.thread.start()

    def __setstate__(self, state):
        """Re-initialize the class."""
        self.__init__(**state)

    def restart_listener(self, topics):
        """Restart listener after configuration update."""
        if self.listener is not None:
            if self.listener.running:
                self.stop()
        self.__init__(topics=topics)

    def stop(self):
        """Stop listener."""
        self.logger.debug('Stopping listener.')
        self.listener.stop()
        if self.thread is not None:
            self.thread.join()
            self.thread = None
        self.logger.debug('Listener stopped.')