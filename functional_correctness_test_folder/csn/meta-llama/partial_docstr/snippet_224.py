
class Host:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"Host('{self.name}', '{self.description}')"


class HostManager:
    def __init__(self):
        self.hosts = {}

    def get_hosts(self):
        '''
        Retrieves a list of all hosts.
        '''
        return list(self.hosts.values())

    def get_host(self, host: str):
        '''
        Retrieves a specific host by name.
        '''
        return self.hosts.get(host)

    def modify_host(self, host: str, description: str) -> Host:
        '''
        Modifies description of a specific host.
        '''
        if host in self.hosts:
            self.hosts[host].description = description
        return self.hosts.get(host)


# Example usage:
if __name__ == "__main__":
    host_manager = HostManager()
    host_manager.hosts = {
        "host1": Host("host1", "Description for host1"),
        "host2": Host("host2", "Description for host2"),
    }

    print("All hosts:")
    print(host_manager.get_hosts())

    print("\nGet host1:")
    print(host_manager.get_host("host1"))

    print("\nModify host1 description:")
    modified_host = host_manager.modify_host(
        "host1", "New description for host1")
    print(modified_host)

    print("\nAll hosts after modification:")
    print(host_manager.get_hosts())
