
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import re


@dataclass
class UpdateFeedModel:
    feed_id: int
    name: str
    url: str
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not isinstance(self.feed_id, int) or self.feed_id <= 0:
            raise ValueError("feed_id must be a positive integer")
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("name must be a non-empty string")
        if not isinstance(self.url, str) or not self.url.strip():
            raise ValueError("url must be a non-empty string")

        # Basic URL validation
        url_pattern = re.compile(
            r'^(?:http|https)://'
            r'(?:\S+(?::\S*)?@)?'
            r'(?:'
            r'(?P<private_ip>'
            r'(?:(?:10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3})|'
            r'(?:(?:169\.254|192\.168)\.\d{1,3}\.\d{1,3})|'
            r'(?:172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})'
            r')|'
            r'(?P<public_ip>'
            r'(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])'
            r'(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){3}'
            r')|'
            r'(?P<domain>'
            r'(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+'
            r'(?:\.(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)*'
            r'\.(?:[a-z\u00a1-\uffff]{2,})'
            r')'
            r')'
            r'(?::\d{2,5})?'
            r'(?:/\S*)?$', re.IGNORECASE)
        if not url_pattern.match(self.url):
            raise ValueError("url is not a valid URL")

        if self.description is not None and not isinstance(self.description, str):
            raise ValueError("description must be a string")
        if not isinstance(self.tags, list):
            raise ValueError("tags must be a list")
        for tag in self.tags:
            if not isinstance(tag, str):
                raise ValueError("each tag must be a string")

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "feed_id": self.feed_id,
            "name": self.name,
            "url": self.url,
        }
        if self.description is not None:
            result["description"] = self.description
        if self.tags:
            result["tags"] = self.tags
        return result
