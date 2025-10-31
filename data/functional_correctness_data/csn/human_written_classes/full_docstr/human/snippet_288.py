import copy

class Aspect:
    """A network, ansible_host, system, deploy, configure or contextualize element in a RADL."""

    def getId(self):
        """Return the id of the aspect."""
        return id(self)

    def clone(self):
        """Return a copy of this aspect."""
        return copy.deepcopy(self)