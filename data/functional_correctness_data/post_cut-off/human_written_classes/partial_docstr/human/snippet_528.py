from typing import Any, Callable, Dict, List, Optional, Type, Union
from dataclasses import dataclass, field

@dataclass
class RouteInfo:
    """
    Route information
    Contains detailed information about a specific route,
    such as its path, parameters etc...
    """

    def __init__(self, path: str, params: Dict[str, Any]=None, query: Dict[str, Any]=None, data: Dict[str, Any]=field(default_factory=dict), fragment: Optional[str]=None):
        self.path = path
        self.params = params or {}
        self.query = query or {}
        self.data = data
        self.fragment = fragment
        self._extra = {}

    def add_extra(self, key: str, value: Any):
        """
        Adds additional data to the route
        Allows associating additional data with a route, 
        such as metadata, security information, or context data.
        """
        self._extra[key] = value

    def get_extra(self, key: str, default: Any=None) -> Any:
        """
        Gets additional data
        Retrieves the additional data associated with a route, 
        such as metadata, security information, or context data.
        """
        return self._extra.get(key, default)

    @property
    def full_url(self) -> str:
        """Returns the complete URL including query parameters"""
        query_str = '&'.join([f'{k}={v}' for k, v in self.query.items()])
        url = self.path
        if query_str:
            url += f'?{query_str}'
        if self.fragment:
            url += f'#{self.fragment}'
        return url