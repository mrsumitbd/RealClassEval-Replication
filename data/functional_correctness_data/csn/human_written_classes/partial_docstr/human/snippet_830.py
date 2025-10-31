class MatrixServerWellKnown:
    """
    Matrix Server well-known as per https://matrix.org/docs/spec/server_server/r0.1.4#server-discovery
    """

    def __init__(self, homeserver_domain_with_port: str):
        self.homeserver_domain_with_port = homeserver_domain_with_port

    def render(self):
        return {'m.server': self.homeserver_domain_with_port}