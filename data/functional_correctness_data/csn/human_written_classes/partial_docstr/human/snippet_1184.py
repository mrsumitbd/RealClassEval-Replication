from aiohttp import ClientSession
from typing import Any, Optional, TypeVar, Type, Dict

class ConnectionHandler:
    """Helper class used by other API classes to ease passing server connection information."""

    def __init__(self, http_scheme: str, ws_scheme: str, server: str, port: int, path: str, session: ClientSession, proxy: Optional[str]=None) -> None:
        """
        Init instance of connection handler

        :param http_scheme: Http scheme
        :param ws_scheme: Web socket scheme
        :param server: Server IP or domain name
        :param port: Port number
        :param port: Url path
        :param session: Session AIOHTTP
        :param proxy: Proxy (optional, default=None)
        """
        self.http_scheme = http_scheme
        self.ws_scheme = ws_scheme
        self.server = server
        self.port = port
        self.path = path
        self.proxy = proxy
        self.session = session

    def __str__(self) -> str:
        return 'connection info: %s:%d' % (self.server, self.port)