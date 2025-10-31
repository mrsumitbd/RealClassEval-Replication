class DorisClientConfig:
    """Doris client configuration class"""

    def __init__(self, transport: str='stdio', server_command: str | None=None, server_args: list[str] | None=None, server_url: str | None=None, timeout: int=60):
        self.transport = transport
        self.server_command = server_command
        self.server_args = server_args or []
        self.server_url = server_url
        self.timeout = timeout

    @classmethod
    def stdio(cls, command: str, args: list[str]=None) -> 'DorisClientConfig':
        """Create stdio connection configuration"""
        return cls(transport='stdio', server_command=command, server_args=args or [])

    @classmethod
    def http(cls, url: str, timeout: int=60) -> 'DorisClientConfig':
        """Create HTTP connection configuration"""
        return cls(transport='http', server_url=url, timeout=timeout)