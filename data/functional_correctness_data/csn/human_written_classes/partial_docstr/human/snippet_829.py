from typing import Dict

class MatrixClientWellKnown:
    """
    Matrix Client well-known as per https://matrix.org/docs/spec/client_server/r0.6.1#server-discovery
    """

    def __init__(self, homeserver_base_url: str, identity_server_base_url: str=None, other_keys: Dict=None):
        self.homeserver_base_url = homeserver_base_url
        self.identity_server_base_url = identity_server_base_url
        self.other_keys = other_keys

    def render(self):
        doc = {'m.homeserver': {'base_url': self.homeserver_base_url}}
        if self.identity_server_base_url:
            doc['m.identity_server'] = {'base_url': self.identity_server_base_url}
        if self.other_keys:
            doc.update(self.other_keys)
        return doc