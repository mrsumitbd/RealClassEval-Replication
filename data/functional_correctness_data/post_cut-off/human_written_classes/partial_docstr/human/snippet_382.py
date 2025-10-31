from typing import TYPE_CHECKING, Callable, Dict, Iterable, List, MutableMapping, NamedTuple, Optional, Sequence, Tuple, Union
from pipask._vendor.pip._internal.utils.misc import redact_auth_from_url

class IndexContent:
    """Represents one response (or page), along with its URL"""

    def __init__(self, content: bytes, content_type: str, encoding: Optional[str], url: str, cache_link_parsing: bool=True) -> None:
        """
        :param encoding: the encoding to decode the given content.
        :param url: the URL from which the HTML was downloaded.
        :param cache_link_parsing: whether links parsed from this page's url
                                   should be cached. PyPI index urls should
                                   have this set to False, for example.
        """
        self.content = content
        self.content_type = content_type
        self.encoding = encoding
        self.url = url
        self.cache_link_parsing = cache_link_parsing

    def __str__(self) -> str:
        return redact_auth_from_url(self.url)