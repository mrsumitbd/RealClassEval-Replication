from typing import Any, Dict, ItemsView, Iterator, KeysView, List, Optional, Protocol, Set, TypeVar, Union, ValuesView

class BaseAttributes:
    __slots__ = ('hostname', 'password', 'platform', 'port', 'username')

    def __init__(self, hostname: Optional[str]=None, port: Optional[int]=None, username: Optional[str]=None, password: Optional[str]=None, platform: Optional[str]=None) -> None:
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.platform = platform

    @classmethod
    def schema(cls) -> Dict[str, Any]:
        return {'hostname': 'str', 'port': 'int', 'username': 'str', 'password': 'str', 'platform': 'str'}

    def dict(self) -> Dict[str, Any]:
        return {'hostname': object.__getattribute__(self, 'hostname'), 'port': object.__getattribute__(self, 'port'), 'username': object.__getattribute__(self, 'username'), 'password': object.__getattribute__(self, 'password'), 'platform': object.__getattribute__(self, 'platform')}