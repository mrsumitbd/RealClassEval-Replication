
class ListenerContainer:
    '''Container for a listener instance.'''

    def __init__(self, topics=None, addresses=None, nameserver='localhost', services=''):
        '''Initialize the class.'''
        self.topics = topics if topics is not None else []
        self.addresses = addresses if addresses is not None else []
        self.nameserver = nameserver
        self.services = services
        self.listener_active = True

    def __setstate__(self, state):
        '''Re-initialize the class.'''
        self.__dict__.update(state)
        self.listener_active = True

    def restart_listener(self, topics):
        '''Restart listener after configuration update.'''
        self.topics = topics
        self.listener_active = False
        # Simulate restart
        self.listener_active = True

    def stop(self):
        '''Stop listener.'''
        self.listener_active = False
