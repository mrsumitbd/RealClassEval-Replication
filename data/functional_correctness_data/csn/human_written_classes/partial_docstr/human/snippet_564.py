from lxml.etree import _Element
from typing import Any, Dict, List, Optional, Union
from lxml import etree as et

class XMLTree:
    """A generic tree representation which takes XML as input.

    Includes subroutines for conversion to JSON & for visualization based on js
    form
    """

    def __init__(self, xml_root: _Element, words: Optional[List[str]]=None) -> None:
        """Call subroutines to generate JSON form of XML input."""
        self.root = xml_root
        self.words = words
        self.id = str(abs(hash(self.to_str())))

    def _to_json(self, root: _Element) -> Dict:
        children: List[Dict] = []
        for c in root:
            children.append(self._to_json(c))
        js = {'attrib': dict(root.attrib), 'children': children}
        return js

    def to_json(self) -> Dict:
        """Convert to json."""
        return self._to_json(self.root)

    def to_str(self) -> bytes:
        """Convert to string."""
        return et.tostring(self.root)