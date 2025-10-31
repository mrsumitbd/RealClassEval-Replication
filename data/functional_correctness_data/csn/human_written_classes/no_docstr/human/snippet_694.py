class VirtualHost:

    def __init__(self, fqdn, ip, network_id, port):
        self.fqdn = fqdn
        self.ip = ip
        self.network_id = network_id
        self.port = port

    def __repr__(self):
        return f'vhost: {self.fqdn}, ip: {self.ip}, network_id: {self.network_id}, port: {self.port}'