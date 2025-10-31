class Nerve:
    """Base class for implementations of a nerve finder to build a Mapper complex."""

    def __init__(self):
        pass

    def compute(self, nodes, links):
        raise NotImplementedError()