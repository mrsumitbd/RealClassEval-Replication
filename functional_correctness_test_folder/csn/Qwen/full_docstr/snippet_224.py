
class HostManager:
    '''
    Functions for managing hosts. Intended to be used as a mixin for CloudManager.
    '''

    def get_hosts(self):
        '''
        Returns a list of available hosts, along with basic statistics of them when available.
        '''
        # Implementation for getting a list of hosts
        return [{'host_id': 'host1', 'status': 'active', 'cpu_usage': 20, 'memory_usage': 30},
                {'host_id': 'host2', 'status': 'inactive', 'cpu_usage': 0, 'memory_usage': 0}]

    def get_host_details(self, host_id: str):
        '''
        Returns detailed information about a specific host.
        '''
        # Implementation for getting detailed information about a specific host
        if host_id == 'host1':
            return {'host_id': 'host1', 'status': 'active', 'cpu_usage': 20, 'memory_usage': 30, 'description': 'Main server'}
        elif host_id == 'host2':
            return {'host_id': 'host2', 'status': 'inactive', 'cpu_usage': 0, 'memory_usage': 0, 'description': 'Backup server'}
        else:
            return None

    def modify_host(self, host_id: str, description: str) -> dict:
        '''
        Modifies description of a specific host.
        '''
        # Implementation for modifying the description of a specific host
        if host_id == 'host1':
            return {'host_id': 'host1', 'status': 'active', 'cpu_usage': 20, 'memory_usage': 30, 'description': description}
        elif host_id == 'host2':
            return {'host_id': 'host2', 'status': 'inactive', 'cpu_usage': 0, 'memory_usage': 0, 'description': description}
        else:
            return None
