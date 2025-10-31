import os

class SockPath:
    """Describes how to connect to watchman"""
    unix_domain = None
    named_pipe = None
    tcp_address = None

    def __init__(self, unix_domain=None, named_pipe=None, sockpath=None, tcp_address=None):
        if named_pipe is None and sockpath is not None and is_named_pipe_path(sockpath):
            named_pipe = sockpath
        if unix_domain is None and sockpath is not None and (not is_named_pipe_path(sockpath)):
            unix_domain = sockpath
        self.unix_domain = unix_domain
        self.named_pipe = named_pipe
        self.tcp_address = tcp_address

    def legacy_sockpath(self):
        """Returns a sockpath suitable for passing to the watchman
        CLI --sockname parameter"""
        log('legacy_sockpath called: %r', self)
        if os.name == 'nt':
            return self.named_pipe
        return self.unix_domain