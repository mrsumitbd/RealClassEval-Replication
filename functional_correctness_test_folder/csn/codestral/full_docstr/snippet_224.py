
class HostManager:
    '''
    Functions for managing hosts. Intended to be used as a mixin for CloudManager.
    '''

    def get_hosts(self):
        '''
        Returns a list of available hosts, along with basic statistics of them when available.
        '''
        hosts = []
        # Implementation to fetch hosts and their basic statistics
        # Example: hosts = self._fetch_hosts_basic_stats()
        return hosts

    def get_host_details(self, host: str):
        '''
        Returns detailed information about a specific host.
        '''
        host_details = {}
        # Implementation to fetch detailed information about the host
        # Example: host_details = self._fetch_host_details(host)
        return host_details

    def modify_host(self, host: str, description: str) -> Host:
        '''
        Modifies description of a specific host.
        '''
        # Implementation to modify the host's description
        # Example: self._update_host_description(host, description)
        modified_host = Host(host, description)
        return modified_host


class Host:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
