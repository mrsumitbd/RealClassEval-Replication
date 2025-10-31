
class Host:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"Host(name={self.name}, description={self.description})"


class HostManager:
    def __init__(self):
        self.hosts = {}

    def get_hosts(self) -> list[Host]:
        return list(self.hosts.values())

    def modify_host(self, host: str, description: str) -> Host:
        if host in self.hosts:
            self.hosts[host].description = description
        else:
            self.hosts[host] = Host(host, description)
        return self.hosts[host]
