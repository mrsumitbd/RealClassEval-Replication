
from typing import List, Dict


class Host:
    def __init__(self, name: str, description: str, stats: Dict = None):
        self.name = name
        self.description = description
        self.stats = stats

    def __repr__(self):
        return f"Host(name='{self.name}', description='{self.description}', stats={self.stats})"


class HostManager:
    '''
    Functions for managing hosts. Intended to be used as a mixin for CloudManager.
    '''

    def __init__(self, hosts_data: Dict = None):
        self.hosts_data = hosts_data if hosts_data else {}

    def get_hosts(self) -> List[Host]:
        '''
        Returns a list of available hosts, along with basic statistics of them when available.
        '''
        hosts = []
        for name, data in self.hosts_data.items():
            hosts.append(
                Host(name, data.get('description'), data.get('stats')))
        return hosts

    def get_host(self, host: str) -> Host:
        '''
        Returns detailed information about a specific host.
        '''
        host_data = self.hosts_data.get(host)
        if host_data:
            return Host(host, host_data.get('description'), host_data)
        else:
            raise ValueError(f"Host '{host}' not found")

    def modify_host(self, host: str, description: str) -> Host:
        '''
        Modifies description of a specific host.
        '''
        if host in self.hosts_data:
            self.hosts_data[host]['description'] = description
            return self.get_host(host)
        else:
            raise ValueError(f"Host '{host}' not found")


# Example usage:
if __name__ == "__main__":
    hosts_data = {
        'host1': {'description': 'Host 1', 'stats': {'cpu': 50, 'mem': 60}},
        'host2': {'description': 'Host 2', 'stats': {'cpu': 30, 'mem': 70}}
    }

    host_manager = HostManager(hosts_data)

    print("Available hosts:")
    for host in host_manager.get_hosts():
        print(host)

    print("\nDetailed info about 'host1':")
    print(host_manager.get_host('host1'))

    print("\nModifying 'host1' description:")
    modified_host = host_manager.modify_host(
        'host1', 'New description for Host 1')
    print(modified_host)
