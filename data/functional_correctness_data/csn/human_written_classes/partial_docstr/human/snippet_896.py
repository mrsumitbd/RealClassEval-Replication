from draftjs_exporter.types import HTML, Tag
from draftjs_exporter.engines.base import Attr, DOMEngine
from typing import List, Optional, Sequence, Union

class Elt:
    """
    A DOM element that the string engine manipulates.
    This class doesn't do much, but the exporter relies on
    comparing elements by reference so it's useful nonetheless.
    """
    __slots__ = ('type', 'attr', 'children', 'markup')

    def __init__(self, type_: Tag, attr: Optional[Attr], markup: HTML=''):
        self.type = type_
        self.attr = attr
        self.children: List['Elt'] = []
        self.markup = markup

    @staticmethod
    def from_html(markup: HTML) -> 'Elt':
        return Elt('escaped_html', None, markup)