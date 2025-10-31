import ipaddress

class _TrustedHosts:
    """Container for trusted hosts and networks"""

    def __init__(self, trusted_hosts: list[str] | str) -> None:
        self.always_trust: bool = trusted_hosts in ('*', ['*'])
        self.trusted_literals: set[str] = set()
        self.trusted_hosts: set[ipaddress.IPv4Address | ipaddress.IPv6Address] = set()
        self.trusted_networks: set[ipaddress.IPv4Network | ipaddress.IPv6Network] = set()
        if not self.always_trust:
            if isinstance(trusted_hosts, str):
                trusted_hosts = _parse_raw_hosts(trusted_hosts)
            for host in trusted_hosts:
                if '/' in host:
                    try:
                        self.trusted_networks.add(ipaddress.ip_network(host))
                    except ValueError:
                        self.trusted_literals.add(host)
                else:
                    try:
                        self.trusted_hosts.add(ipaddress.ip_address(host))
                    except ValueError:
                        self.trusted_literals.add(host)

    def __contains__(self, host: str | None) -> bool:
        if self.always_trust:
            return True
        if not host:
            return False
        try:
            ip = ipaddress.ip_address(host)
            if ip in self.trusted_hosts:
                return True
            return any((ip in net for net in self.trusted_networks))
        except ValueError:
            return host in self.trusted_literals

    def get_trusted_client_host(self, x_forwarded_for: str) -> str:
        """Extract the client host from x_forwarded_for header

        In general this is the first "untrusted" host in the forwarded for list.
        """
        x_forwarded_for_hosts = _parse_raw_hosts(x_forwarded_for)
        if self.always_trust:
            return x_forwarded_for_hosts[0]
        for host in reversed(x_forwarded_for_hosts):
            if host not in self:
                return host
        return x_forwarded_for_hosts[0]