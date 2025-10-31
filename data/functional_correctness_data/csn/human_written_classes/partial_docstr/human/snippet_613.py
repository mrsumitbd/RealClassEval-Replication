import json
from typing import Any, Dict, Iterable, List, Mapping, Optional, Set, Type, Union

class FakeReq:
    """A Fake Request is used for compatible error reporting in "composite" subrequests."""

    def __init__(self, method: str, url: str, data: str, headers: Optional[Dict[str, str]]=None, context: Optional[Dict[Any, Any]]=None) -> None:
        self.method = method
        self.url = url
        self.data = data
        self.headers = headers or {}
        self.context = context or {}

    @property
    def body(self) -> str:
        if isinstance(self.data, str):
            return self.data
        return json.dumps(self.data)