
class Host:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"Host('{self.name}', '{self.description}')"


class HostManager:
    def __init__(self):
        self.hosts = {}

    def get_hosts(self) -> dict:
        return self.hosts

    def get_host(self, host: str) -> Host:
        return self.hosts.get(host)

    def modify_host(self, host: str, description: str) -> Host:
        if host in self.hosts:
            self.hosts[host].description = description
        else:
            self.hosts[host] = Host(host, description)
        return self.hosts[host]


# Example usage:
if __name__ == "__main__":
    manager = HostManager()
    manager.modify_host("localhost", "Local Host")
    # Output: Host('localhost', 'Local Host')
    print(manager.get_host("localhost"))
    # Output: {'localhost': Host('localhost', 'Local Host')}
    print(manager.get_hosts())
