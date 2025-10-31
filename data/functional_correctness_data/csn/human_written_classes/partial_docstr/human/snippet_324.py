from sen.util import graceful_chain_get

class NetData:

    def __init__(self, inspect_data):
        self.inspect_data = inspect_data
        self.net_settings = graceful_chain_get(self.inspect_data, 'NetworkSettings')
        self._ports = None
        self._ips = None

    @property
    def ports(self):
        """
        :return: dict
            {
                # container -> host
                "1234": "2345"
            }
        """
        if self._ports is None:
            self._ports = {}
            if self.net_settings['Ports']:
                for key, value in self.net_settings['Ports'].items():
                    cleaned_port = key.split('/')[0]
                    self._ports[cleaned_port] = graceful_chain_get(value, 0, 'HostPort')
            exposed_ports_section = graceful_chain_get(self.inspect_data, 'HostConfig', 'PortBindings')
            if exposed_ports_section:
                for key, value in exposed_ports_section.items():
                    cleaned_port = key.split('/')[0]
                    if cleaned_port not in self._ports:
                        self._ports[cleaned_port] = graceful_chain_get(value, 0, 'HostPort')
            exposed_ports_section = graceful_chain_get(self.inspect_data, 'Config', 'ExposedPorts')
            if exposed_ports_section:
                for key, value in exposed_ports_section.items():
                    cleaned_port = key.split('/')[0]
                    if cleaned_port not in self._ports:
                        self._ports[cleaned_port] = None
        return self._ports

    @property
    def ips(self):
        """
        :return: dict:
        {
            "default": {
                "ip_address4": "12.34.56.78"
                "ip_address6": "ff:fa:..."
            }
            "other": {
                ...
            }
        }
        """
        if self._ips is None:
            self._ips = {}
            default_net = extract_data_from_inspect('default', self.net_settings)
            if default_net:
                self._ips['default'] = default_net
            networks = self.inspect_data['NetworkSettings']['Networks']
            if networks:
                for network_name, network_data in networks.items():
                    self._ips[network_name] = extract_data_from_inspect(network_name, network_data)
        return self._ips