class Node:
    """Base class for objects that represent a single object in the BIDS
    hierarchy.

    Parameters
    ----------
    id : int or str
        A value uniquely identifying this node. Typically the
        entity value extracted from the filename via layout.
    """

    def __init__(self, level, entities):
        self.level = level.lower()
        self.entities = entities
        if self.entities is not None:
            self.base_ents = {e: val for e, val in entities.items() if e in BASE_ENTITIES}
        else:
            self.base_ents = None
        self.variables = {}

    def add_variable(self, variable):
        """Adds a BIDSVariable to the current Node's list.

        Parameters
        ----------
        variable : BIDSVariable
            The Variable to add to the list.
        """
        if self.base_ents is not None:
            for e, val in self.base_ents.items():
                if e in variable.entities and variable.entities[e] != val:
                    raise ValueError('Variable and node entity mismatch.')
        self.variables[variable.name] = variable