
class Host:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"Host(name={self.name!r}, description={self.description!r})"


class HostManager:
    def __init__(self):
        self._hosts = {}

    def get_hosts(self):
        return list(self._hosts.values())

    def modify_host(self, host: str, description: str) -> Host:
        if host in self._hosts:
            self._hosts[host].description = description
        else:
            self._hosts[host] = Host(host, description)
        return self._hosts[host]
