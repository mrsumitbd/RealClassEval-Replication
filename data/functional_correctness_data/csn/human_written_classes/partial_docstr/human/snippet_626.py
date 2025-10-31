from pliers.transformers import get_transformer

class Node:
    """ A graph node/vertex. Represents a single transformer, optionally with
    references to children.

    Args:
        name (str): Name of the node
        transformer (Transformer): the Transformer instance at this node
        parameters (kwargs): parameters for initializing the Transformer
    """

    def __init__(self, transformer, name=None, **parameters):
        self.name = name
        self.children = []
        if isinstance(transformer, str):
            transformer = get_transformer(transformer, **parameters)
        self.transformer = transformer
        self.parameters = parameters
        if name is not None:
            self.transformer.name = name
        self.id = id(transformer)

    def add_child(self, node):
        """ Append a child to the list of children. """
        self.children.append(node)

    def is_leaf(self):
        return len(self.children) == 0

    def to_json(self):
        spec = {'transformer': self.transformer.__class__.__name__}
        if self.name:
            spec['name'] = self.name
        if self.children:
            children = []
            for c in self.children:
                children.append(c.to_json())
            spec['children'] = children
        if self.parameters:
            spec['parameters'] = self.parameters
        return spec