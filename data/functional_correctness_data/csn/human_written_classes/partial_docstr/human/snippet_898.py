from typing import List, Optional, Sequence, Union
from draftjs_exporter.options import Options, OptionsMap
from draftjs_exporter.types import Block, Element, Props, RenderableType
from draftjs_exporter.dom import DOM

class Wrapper:
    """
    A wrapper is an element that wraps other nodes. It gets created
    when the depth of a block is different than 0, so the DOM elements
    have the appropriate amount of nesting.
    """
    __slots__ = ('depth', 'last_child', 'type', 'props', 'elt')

    def __init__(self, depth: int, options: Optional[Options]=None) -> None:
        self.depth = depth
        self.last_child = None
        if options:
            self.type = options.wrapper
            self.props = options.wrapper_props
            wrapper_props = dict(self.props) if self.props else {}
            wrapper_props['block'] = {'type': options.type, 'depth': depth}
            self.elt = DOM.create_element(self.type, wrapper_props)
        else:
            self.type = None
            self.props = None
            self.elt = DOM.create_element()

    def is_different(self, depth: int, type_: RenderableType, props: Optional[Props]) -> bool:
        return depth > self.depth or type_ != self.type or props != self.props