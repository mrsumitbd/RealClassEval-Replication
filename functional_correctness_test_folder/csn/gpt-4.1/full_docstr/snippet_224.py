
class Host:
    def __init__(self, name, description='', stats=None, details=None):
        self.name = name
        self.description = description
        self.stats = stats or {}
        self.details = details or {}

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'stats': self.stats,
            'details': self.details
        }


class HostManager:
    '''
    Functions for managing hosts. Intended to be used as a mixin for CloudManager.
    '''

    def __init__(self):
        # Simulate a host database as a dict: host_name -> Host instance
        self._hosts = {
            'host1': Host('host1', 'Primary host', {'cpu': 80, 'mem': 64}, {'os': 'Linux', 'ip': '10.0.0.1'}),
            'host2': Host('host2', 'Backup host', {'cpu': 40, 'mem': 32}, {'os': 'Linux', 'ip': '10.0.0.2'}),
            'host3': Host('host3', 'Test host', {'cpu': 20, 'mem': 16}, {'os': 'Windows', 'ip': '10.0.0.3'}),
        }

    def get_hosts(self):
        '''
        Returns a list of available hosts, along with basic statistics of them when available.
        '''
        hosts_list = []
        for host in self._hosts.values():
            hosts_list.append({
                'name': host.name,
                'description': host.description,
                'stats': host.stats
            })
        return hosts_list

    def get_host(self, host_name):
        '''
        Returns detailed information about a specific host.
        '''
        host = self._hosts.get(host_name)
        if not host:
            return None
        return {
            'name': host.name,
            'description': host.description,
            'stats': host.stats,
            'details': host.details
        }

    def modify_host(self, host: str, description: str) -> Host:
        '''
        Modifies description of a specific host.
        '''
        if host not in self._hosts:
            raise ValueError(f"Host '{host}' not found.")
        self._hosts[host].description = description
        return self._hosts[host]
