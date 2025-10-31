from collections import OrderedDict, deque

class Example:
    """An example of a struct or union type."""

    def __init__(self, label, text, value, ast_node=None):
        assert isinstance(label, str), type(label)
        self.label = label
        assert isinstance(text, (str, type(None))), type(text)
        self.text = doc_unwrap(text) if text else text
        assert isinstance(value, (str, OrderedDict)), type(value)
        self.value = value
        self._ast_node = ast_node

    def __repr__(self):
        return 'Example({!r}, {!r}, {!r})'.format(self.label, self.text, self.value)