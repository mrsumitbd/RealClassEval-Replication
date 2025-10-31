
class HostManager:
    '''
    Functions for managing hosts. Intended to be used as a mixin for CloudManager.
    '''

    def get_hosts(self):
        '''
        Returns a list of available hosts, along with basic statistics of them when available.
        '''
        pass

    def get_host(self, host: str):
        '''
        Returns detailed information about a specific host.
        '''
        pass

    def modify_host(self, host: str, description: str):
        '''
        Modifies description of a specific host.
        '''
        pass
